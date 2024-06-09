#include <WiFi.h>
#include <ESPAsyncWebSrv.h>
#include<FastLED.h>

#define LED_PIN1     26
#define LED_PIN2     13
#define LED_PIN3     14
#define LED_PIN4     33

#define NUM_LEDS    900
String s="";
CRGB leds[4][NUM_LEDS];
//int index =0;
const char* ssid = "Professor";
const char* password = "myyz7575";
const int rows = 3;
const int cols = 900;

// Create a 2D array
int dataArray[rows][cols];

AsyncWebServer server(80);

IPAddress serverIP(192,168,51,147);  

void setup() {
 
  Serial.begin(57600);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  // server.begin();
  server.on("/send-array", HTTP_POST, handleArray);
  
  server.begin();
  FastLED.addLeds<WS2812, LED_PIN1, GRB>(leds[0], NUM_LEDS);
  FastLED.addLeds<WS2812, LED_PIN2, GRB>(leds[1], NUM_LEDS);
  FastLED.addLeds<WS2812, LED_PIN3, GRB>(leds[2], NUM_LEDS);
  FastLED.addLeds<WS2812, LED_PIN4, GRB>(leds[3], NUM_LEDS);
  //Serial.println(WiFi.localIP());
}

void loop(){
  FastLED.show();
}


void led_set(int x,int y,int color[3] )
{
    float c=67.5;//y 41 k 10 l 1
    int j=0;
    int l;
    int layer_size = 900;
    int led=0;
    int k=x/4;// same layer x
    l=x%4;//layer
    int strip_no = k/4;
    // Serial.print(x);
    // Serial.println(y);

  if (l %2 == 0){
      
      int flip_x = k%2 ;
      leds[l] [(int)( y  + (k*c)+ flip_x*c - 2*flip_x*y +10*k -strip_no*10 )] =CRGB(color[0],color[1],color[2]) ;
    }
    else if (l %2 == 1){
      
      int flip_x = k%2 ;
      leds[l] [(int)(  layer_size-( y+ (k*c)+ flip_x*c - 2*flip_x*y +10*k -strip_no*10))]=CRGB(color[0],color[1],color[2]);
      }
}

void handleArray(AsyncWebServerRequest *request){
  Serial.println("Handling Array Request");
  
  if(request->hasParam("data", true)){
    String data = request->getParam("data", true)->value();
    Serial.print("Received Data: ");
    Serial.println(data);
    
    int index=0;
    //int index = 0;
    int rgbValues[3];
    // Parse the received data into the dataArray
    String chunk= "";
    int pixelNo = 0;
    int c  = data[0] - '0';
    for (int i = 1; i < data.length(); i++) {
        if (data[i] == ',' || i==data.length()-1) 
        {
          rgbValues[index%3] = chunk.toInt();
          Serial.print( rgbValues[index%3]);
          Serial.print(",");
          index++;
          chunk = "";
         
          if(index%3==0)
          {
            pixelNo = index/3;
            Serial.print("  ");
            led_set(pixelNo%(48) , (pixelNo/(48)) +11*c , rgbValues );
            // leds[(index-3)/3]=CRGB(rgbValues[0],rgbValues[1],rgbValues[2]);
            // FastLED.show();
          }
        } 
        else {
          chunk += data[i];
        }
        
    }


    // Send a response to the client with ESP32 IP address
    String responseMsg = "Array received successfully from ESP32 at IP: " + WiFi.localIP().toString();
    Serial.println("\n"+responseMsg);

    request->send(200, "text/plain", responseMsg);
  }
  else {
    Serial.println("No 'data' parameter found");
    request->send(400, "text/plain", "Bad Request");
  }
}
