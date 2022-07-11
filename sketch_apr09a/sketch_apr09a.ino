int sensor_0_aver[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int sensor_1_aver[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int sensor_2_aver[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

int sensor_0 = 0;
int sensor_1 = 0;
int sensor_2 = 0;


void setup() 
{
  Serial.begin(9600);
}

int Filter(int sensor_aver[])
{
  int sum = 0;
  for(int a = 0; a<10; a ++)
  {
    sum= sum + sensor_aver[a];
  }
  return sum/10;
}

void Read_from_sensor()
{
  for(int i =0; i<10; i++)
  {
     sensor_0_aver[i]=analogRead(0);
     sensor_1_aver[i]=analogRead(1);
     sensor_2_aver[i]=analogRead(2);
     delay (10);
  }
  sensor_0 = Filter(sensor_0_aver);
  sensor_1 = Filter(sensor_1_aver);
  sensor_2 = Filter(sensor_2_aver);
  
}

void loop() {
  Read_from_sensor();
  String file_ = String(sensor_0)+','+String(sensor_1)+','+String(sensor_2)+',';
 Serial.println(file_);

}
