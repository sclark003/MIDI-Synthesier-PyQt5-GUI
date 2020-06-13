// File: oscillator.cxx

#include <stdio.h>
#include <math.h>
#include <iostream>
#include "oscillator.h"
#define PI 3.14159265

//Function to generate sine wave
void Oscillate::wavesine (double *arr1, std::size_t fs1, float f1)
{
  int i = 0;
  //Set input recursive variable values
  float one = 1;
  float two = 0;
  //Find radial frequency value
  float wT = (2*PI*f1)/fs1; 
  for (int i = 0; i < fs1; i++)
    {
       float acc1 = one * (2*cos(wT));
       float acc2 = two * -1;
       arr1[i] = (acc1 + acc2);
       //Update recursive variables
	   two = one;
       one = arr1[i];
   }
}

//Function to generate square wave
void Oscillate::wavesquare (double *arr2, std::size_t fs2, float f2, float duty)
{
  int i = 0;
  int j = 0;
  float c = float(fs2);
  //Calulate length of one wave cycle
  float len = c/f2;
  //Calulate length of 'up' section of wave based on duty cycle value
  float dutylen = duty*len;
  for (int i = 0; i < fs2; i++)
    {     
	//For each cycle length, set duty cycle percentage of wave as 1
	//And the remainder as -1
	if (j<len)
          {
	     if (j < dutylen)
	       {
	          arr2[i] = 1;
                }
	     if (j> dutylen)
	       {
	          arr2[i]= -1;
	       }
             j++;
	  }
        //Reset for next wave cycle
		if (j>len)
	  {
	     j = 0;
	  }
    }
}
