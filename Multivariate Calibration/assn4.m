clear all;
clc;
load ("Inorfull.mat");

%% Part A
Yavg = [];
Ysample = [];
stdavg = [];
concavg = [];
for i=1:26
    istart = 5*(i-1)+1;
    Ysample = [Ysample; DATA(istart,:)];
    iend = istart+4;
    avg = mean(DATA(istart:iend,:),1);
    stda = mean(stdDATA(istart:iend,:),1)/sqrt(5);
    Yavg = [Yavg; avg];
    stdavg = [stdavg; stda];
    avg = mean(CONC(istart:iend,:),1);
    concavg = [concavg;avg];
end

% Maximum absorbances for Ni, Cr, Co corresponds to array indices 48, 54 and 106 
YsampleMLR = [Ysample(:,48) Ysample(:,54) Ysample(:,106)];
YavgMLR = [Yavg(:,48) Yavg(:,54) Yavg(:,106)];

RMSEsampleMLR = LOOCV_OLS(YsampleMLR,concavg);
%% Normal PCR
Npc=10;
PCR_RMSE=[];
for i=1:Npc
    PCR_RMSE=[PCR_RMSE;LOOCV_PCR(Yavg,concavg,i)];
end
plot(PCR_RMSE);
legend("Ni","Cr","Co");
xlabel("No. of PCs");
ylabel("RMSE values");
%% using stda to scale the data. SCALED_PCR
Y_avg=[];
vary=stda.^2;
for i=1:176
    Y_avg=[Y_avg Yavg(:,i)/vary(i)];
end

Npc=10;
scaled_PCR_RMSE=[];
for i=1:Npc
    scaled_PCR_RMSE=[scaled_PCR_RMSE;LOOCV_PCR(Y_avg,concavg,i)];
end
figure;
plot(scaled_PCR_RMSE);
legend("Ni","Cr","Co");
xlabel("No. of PCs");
ylabel("RMSE values");
%looking at sharp fall from 2 pc to 3 pc and not a big drop for 3 to 4,
%number of pCs is 3.
%% using stdavg to scale the data. MLPCR!
vary=stdavg.^2;
Npc=10;
MLPCR_RMSE=[];
for i=1:Npc
    MLPCR_RMSE=[MLPCR_RMSE;LOOCV_MLPCR(Yavg,concavg,stdavg,i)];%% (Ysample, ConcAvg, StdAvg, k)
end
figure;
plot(MLPCR_RMSE);
legend("Ni","Cr","Co");
xlabel("No. of PCs");
ylabel("RMSE values");
%%
t=table(PCR_RMSE,scaled_PCR_RMSE,MLPCR_RMSE);
disp(t);
%%

function [RMSE]=LOOCV_PCR(X,Y,nPc)
RMSE=0;
for i=1:26
    X_i=[X(1:i-1,:);X(i+1:26,:)];
    Y_i=[Y(1:i-1,:);Y(i+1:26,:)];
    X_S=X_i;
    Y_S=Y_i;
    [U S V]=svd(X_S,"econ");
    v1=V(:,1:nPc);
    T=X_S*v1;
    Bstar=inv(T'*T)*T'*Y_S;
    B=v1*Bstar;
    prederr=Y(i,:)-X(i,:)*B;
    RMSE=RMSE+prederr.*prederr;
end
end

function [RMSE]=LOOCV_OLS(X,Y)
RMSE=0;
for i=1:26
    X_i=[X(1:i-1,:);X(i+1:26,:)];
    Y_i=[Y(1:i-1,:);Y(i+1:26,:)];
    mean_X=[mean(X_i(:,1)),mean(X_i(:,2)),mean(X_i(:,3))];
    mean_Y=[mean(Y_i(:,1)),mean(Y_i(:,2)),mean(Y_i(:,3))];
    X_S=X_i;
    Y_S=Y_i;
    m=inv(X_S'*X_S)*X_S'*Y_S;
    % prederr=m*(X(i,:)-mean_X)'-(Y(i,:)-mean_Y)';
    prederr=Y(i,:)-X(i,:)*m;
    RMSE=RMSE+prederr.*prederr;
end
RMSE = sqrt(RMSE/26);
end

function RMSE = LOOCV_MLPCR(Ysample, ConcAvg, StdAvg, k)
    [nsamples, nspecies] = size(ConcAvg);
    RMSE = zeros(1, nspecies);

    for i = 1:nsamples
        Xsub = [Ysample(1:i-1, :); Ysample(i+1:end, :)]; 
        Ysub = [ConcAvg(1:i-1, :); ConcAvg(i+1:end, :)]; 
        stdsub = [StdAvg(1:i-1, :); StdAvg(i+1:end, :)]; 

        [U,S,V] = MLPCA(Xsub, stdsub, k);

        V1 = V(:, 1:k);
        Tsub = Xsub * V1;

        % Estimate MLPCR model parameters
        B = inv(Tsub' * Tsub) * Tsub' * Ysub;
        % Diagonal matrix containing variance of errors for sample i
        Sinv = inv(diag(StdAvg(i, :)));
        % Prediction for left-out sample
        tpred = Ysample(i, :) * Sinv * V1 * inv(V1' * Sinv * V1);
        % Prediction error for left-out sample
        prederr = ConcAvg(i, :) - tpred * B;
        RMSE = RMSE + prederr .* prederr;
    end
    % Compute RMSE for each choice of the number of principal components
    RMSE = sqrt(RMSE /nsamples);
end


function [U,S,V,SOBJ,ErrFlag] = MLPCA(X,stdX,p);
convlim=1e-10;             % convergence limit
maxiter=20000;             % maximum no. of iterations
XX=X;                      % XX is used for calculations
varX=(stdX.^2);            % convert s.d.'s to variances
[i,j] = find(varX==0);     % find zero errors and convert to large
errmax = max(max(varX));   % errors for missing data
for k=1:length(i);
   varX(i(k),j(k)) = 1e+10*errmax;
end
n=length(XX(1,:));         % the number of columns

[U,S,V]=svd(XX,0);         % Decompose adjusted matrix
U0=U(:,1:p);               % Truncate solution to rank p
count=0;                   % Loop counter
Sold=0;                    % Holds last value of objective function
ErrFlag=-1;                % Loop flag

while ErrFlag<0;
   count=count+1;          % Increment loop counter

   Sobj=0;                             % Initialize sum
   MLX=zeros(size(XX));                % and maximum likelihood estimates
   for i=1:n                            % Loop for each column of XX
      Q=sparse(diag(varX(:,i).^(-1)));  % Inverse of err. cov. matrix
      F=inv(U0'*Q*U0);                    % Intermediate calculation
      MLX(:,i)=U0*(F*(U0'*(Q*XX(:,i))));  % Max. likelihood estimates
      dx=XX(:,i)-MLX(:,i);                % Residual vector
      Sobj=Sobj+dx'*Q*dx;                 % Update objective function
   end

   if rem(count,2)==1                   % Check on odd iterations only
      if (abs(Sold-Sobj)/Sobj)<convlim  % Convergence criterion
         ErrFlag=0;
      elseif count>maxiter              % Excessive iterations?
         ErrFlag=1;
      end
   end

   if ErrFlag<0                  % Only do this part if not done
      Sold=Sobj;                 % Save most recent obj. function     
      [U,S,V]=svd(MLX,0);        % Decompose ML values
      XX=XX';                           % Flip matrix
      varX=varX';                       % and the variances
      n=length(XX(1,:));                % Adjust no. of columns
      U0=V(:,1:p);                      % V becomes U in for transpose
   end
end

[U,S,V]=svd(MLX,0);
U=U(:,1:p);
S=S(1:p,1:p);
V=V(:,1:p);
SOBJ=Sobj;
end