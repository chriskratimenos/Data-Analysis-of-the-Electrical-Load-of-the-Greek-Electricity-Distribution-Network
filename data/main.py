from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from datetime import date
from collections import OrderedDict
from operator import itemgetter
from matplotlib import use
import statistics
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_absolute_percentage_error as err
from sklearn.metrics import mean_squared_error
import requests
import numpy as np
import random
from itertools import cycle
import sys


def main():
    use("TkAgg")
    print("Hello, this is a small program to analyze the Energy Load of the greek power system for a given date, as well as the Forecast of the expected Load.")
    while(True):
        print("\nPlease press 1 if you want to thoroughly analyze a given date.")
        print("Please press 2 if you want to analyze a number of dates.")
        print("Please press 3 if you want to compare Greece with another country for a given date.")
        print("Please enter exit if you want to terminate the program.")
        scan=input("Please enter your choice: ")
        if(scan=='1'):
            First()
        elif(scan=='2'):
            number=input("Please enter how  many dates you want to analyze: ")
            try :
                Second(int(number))
            except:
                print("Something went wrong")
                pass
        elif(scan=='3'):
            Third()
        elif(scan.lower()=='exit'):
            break
        else:
            print("\n\nSomething went wrong\n")
            pass

#General Functions for all:

def scanner():
    while(True):
        dates = input("Please enter date after in DD.MM.YYYY format: ")
        list = load(dates)
        try:
            a=len(list)
        except:
            list=load(dates)
        if a==48 and list[-1].isdigit() and list[-2].isdigit():
            break
    return list,dates

def load(date):
    a=f'https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime={date}+00:00|EET|DAY&biddingZone.values=CTY|10YGR-HTSO-----Y!BZN|10YGR-HTSO-----Y&dateTime.timezone=EET_EEST&dateTime.timezone_input=EET+(UTC+2)+/+EEST+(UTC+3)'
    html_text=requests.get(a).text
    soup= BeautifulSoup(html_text,'lxml')
    data=soup.find_all('td',class_="dv-value-cell")
    list_1=[]
    for i in data:
        list_1.append(i.text)
    return list_1

def print_values(list):
    print("TIME     SPECULATION   REAL")
    for o in range(len(list)):
        if(o%2==0):
            if((int(o / 2) + 1) == 10):
                print(f'{int(o / 2)}-{int(o / 2 + 1)}:       {list[o]}     ', format(list[o + 1]))
            elif ((int(o / 2) + 1) > 9):
                print(f'{int(o / 2)}-{int(o / 2 + 1)}:      {list[o]}     ', format(list[o + 1]))

            else:
                print(f'{int(o/2)}-{int(o/2+1)}:        {list[o]}     ',format(list[o+1]))

def get_real(list):
    real=[]
    for i in range(1,len(list),2):
        try:
            real.append(int(list[i]))
        except ValueError:
            sys.exit('Incomplete Data')
    return real

def get_spec(list):
    spec=[]
    for i in range(0,len(list),2):
        try:
            spec.append(int(list[i]))
        except ValueError:
            sys.exit('Incomplete Data')
    return spec

def find_date(dates):
    day, month, year = dates.split('.')
    day_name = date(int(year), int(month), int(day))
    return day_name.strftime("%A")

def percent_error(real,spec):
    error=[]
    for i in range(len(real)):
        error.append(round(((-real[i]+spec[i])/real[i])*100,2))
    return error

class First():
    def __init__(self):
        # Import the date
        list,dates=scanner()
        day, month, year = dates.split('.')
        day_name = date(int(year), int(month), int(day))
        print(f'The day is a {day_name.strftime("%A")}')

        print_values(list)
        #Find the Actual Load
        real=get_real(list)
        # Find the Forecast Load
        spec=get_spec(list)
        #Find the Mean
        mean_real=[statistics.mean(real)]*len(real)
        mean_spec=[statistics.mean(spec)]*len(spec)
        error = percent_error(real,spec)
        while(True):
            print("\nPlease enter a number from 1 to 16:\n1: A line graph of both Actual and Forecast of the load values.")
            print("2: A bar chart of both Actual and Day-ahead Total Forecast of the load values.")
            print("3: A bar chart of the Actual load value.")
            print("4: A bar chart of the Day-ahead Total Load Forecast.")
            print("5: A line graph of the % of error of our Forecast.")
            print("6: A line graph of the % of accuracy of our Forecast.")
            print("7: A line graph of load per hour as a percentage of maximum daily energy load.")
            print("8: Print the Mean Absolute Error.")
            print("9: Print the Mean Absolute Percentage Error")
            print("10: Print the Standard Deviation of the Actual Load.")
            print("11: Print the Mean Squared Error")
            print("12: Print the Mean value of the Actual Load.")
            print("13: Print the Mean value of the Day-ahead Total Load Forecast.")
            print("14: Print the Median value of the Actual Load.")
            print("15: Print the Median value of the Day-ahead Total Load Forecast.")
            print("16: A line graph of the normal distribution of the Actual Total Load.")
            print("To end the program just enter 'End' or 'Telos'.")
            scan = input("Please enter your choice: ")
            print('\n')
            if(scan=='1'):
                self.graph(real, spec,mean_real,mean_spec)
            elif(scan=='2'):
                self.bar_chart_both(real, spec, mean_real, mean_spec)
            elif(scan=='3'):
                self.bar_chart_real(real,mean_real)
            elif(scan=='4'):
                self.bar_chart_forecast(spec,mean_spec)
            elif (scan=='5'):
                self.percent_error_show(error)
            elif (scan=='6'):
                self.percent_accuracy_show(error)
            elif(scan=='7'):
                self.peak_energy_load(real)
            elif(scan=='8'):
                print(f'The Mean Absolute error is: {round(mae(real,spec),3)} MW')
            elif(scan=='9'):
                print(f'The Mean Absolute percentage % Error is: {round(err(real, spec) * 100, 3)}%')
            elif(scan=='10'):
                print(f'The Standard Deviation of the Actual Load is: {round(statistics.stdev(real), 3)}')
            elif(scan=='11'):
                print(f'The Mean Squared Error is: {round(mean_squared_error(real, spec),3)}')
            elif(scan=='12'):
                print(f'The Mean value of the Actual Load is: {round(mean_real[0],3)} MW')
            elif(scan=='13'):
                print(f'The Mean value of the Day-ahead Total Load Forecast is: {round(mean_spec[0],3)} MW')
            elif(scan=='14'):
                print(f'The Median value of the Actual Load is: {round(statistics.median(real),3)} MW')
            elif(scan=='15'):
                print(f'The Median value of the Day-ahead Total Load Forecast is: {round(statistics.median(spec),3)} MW')
            elif(scan=='16'):
                self.normal_distribution(real, mean_real[0])
            elif(scan.lower()=="end" or scan.lower()=="telos"):
                break
            else:
                print("Something went wrong\n")
                pass

    # A graph of the percentage of Error of the Actual Load
    def percent_error_show(self,error):
        loc = plticker.MultipleLocator(base=1.0)
        time=[x for x in range(24)]
        plt.figure(figsize=(10,4))
        plt.plot(time,error,label='Error',color='red',linewidth='2',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='red')
        plt.title("How off was the Forecast? [The % of error between the Forecast Load and the Actual Load]",fontdict={'fontname' : 'Times New Roman', 'fontsize': 16})
        plt.ylabel('Error %',fontdict={'fontname' : 'Times New Roman'})
        plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman'})
        plt.xticks([x for x in range(24)])
        plt.ylim(-20, 20)

        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)

        plt.tight_layout()
        plt.legend()
        plt.show()

    # A graph of the percentage of Accuracy of the Actual Load
    def percent_accuracy_show(self,error):
        accuracy=[]
        for i in error:
            accuracy.append(100-abs(i))
        time=[x for x in range(24)]
        loc = plticker.MultipleLocator(base=1.0)
        plt.figure(figsize=(10,4))
        plt.plot(time,accuracy,label='Accuracy',color='red',linewidth='2',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='red')
        plt.title("How close was the Forecast? [Forecast as a % of the real value]",fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})
        plt.ylabel('ERROR',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman'})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()
        plt.show()

    # A graph of the Actual Load and the Day-Ahead Forecast
    def graph(self,real, spec,mean_real,mean_spec):
        loc = plticker.MultipleLocator(base=1.0)
        time=[x for x in range(24)]
        plt.figure(figsize=(10,4))
        plt.plot(time, mean_real, label='Mean of Actual Total Load', linestyle='dashdot',color='yellow')
        plt.plot(time, mean_spec, label='Mean of Day-ahead Total Load Forecast', linestyle='--',color='green')
        plt.plot(time,spec,label='Total Load Forecast',color='blue',linewidth='2',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='blue')
        plt.plot(time,real,label='Actual Total Load ',color='red',linewidth='2',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='red')
        plt.title("Load: Day-ahead [Total Load Forecast] vs [Actual Total Load]",fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Load [MW]',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()

        plt.show()

    # A bar chart of the Actual Load
    def bar_chart_real(self,real,mean_real):
        loc = plticker.MultipleLocator(base=1.0)
        time=[x for x in range(24)]
        plt.figure(figsize=(10,4))
        bars= plt.bar(time,real,edgecolor='black')
        plt.plot(time,real,label='Actual Total Load',color='black',linewidth='1',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='black')
        plt.plot(time, mean_real, label='Mean', linestyle='--',color='purple')

        plt.title("Load [Actual Total Load]",fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})
        plt.xticks([x for x in range(24)])
        plt.ylabel('Load [MW]',fontdict={'fontname' : 'Times New Roman', 'fontsize': 10})
        plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman', 'fontsize': 10})
        max_value=max(real)
        max_index =  real.index(max_value)
        bars[max_index].set_color('r')
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)

        min_value=min(real)
        min_index =  real.index(min_value)
        bars[min_index].set_color('green')
        plt.tight_layout()
        plt.legend()
        plt.show()

    # A bar chart of the Day-Ahead Forecast Load
    def bar_chart_forecast(self,spec,mean_spec):
        loc = plticker.MultipleLocator(base=1.0)

        time=[x for x in range(24)]
        plt.figure(figsize=(10,4))
        bars= plt.bar(time,spec,edgecolor='black')
        plt.plot(time,spec,label='Total Load Forecast',color='black',linewidth='1',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='black')
        plt.plot(time, mean_spec, label='Mean', linestyle='--',color='purple')

        plt.title("Load [Total Load Forecast]",fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})
        plt.xticks([x for x in range(24)])
        plt.ylabel('Load [MW]',fontdict={'fontname' : 'Times New Roman', 'fontsize': 10})
        plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman', 'fontsize': 10})

        max_value=max(spec)
        max_index =  spec.index(max_value)
        bars[max_index].set_color('r')
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)

        min_value=min(spec)
        min_index =  spec.index(min_value)
        bars[min_index].set_color('green')

        plt.tight_layout()
        plt.legend()

        plt.show()

    # A graph of the the Actual Load as a a percentage of the peak Actual Load
    def peak_energy_load(self,real):
        loc = plticker.MultipleLocator(base=1.0)
        maximum =  real.index(max(real))
        list=[]
        for i in real:
            list.append(round(i/real[maximum]*100,3))
        time=[x for x in range(24)]
        plt.figure(figsize=(10,4))
        plt.plot(time,list,label='Value percent %',color='red',linewidth='2',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='red')

        plt.title("Load per hour as a percentage of maximum daily energy load",fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Load %',fontdict={'fontname' : 'Times New Roman'})
        plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman'})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()
        plt.show()

    # A bar chart of the Actual Load and the Day-Ahead Forecast Load
    def bar_chart_both(self,real,spec,mean_real,mean_spec):
        loc = plticker.MultipleLocator(base=1.0)
        time=[x for x in range(24)]
        width=np.min(np.diff(time))/3
        fig=plt.figure(figsize=(10,4))
        ax=fig.add_subplot(111)
        plt.plot(time, mean_real, label='Mean of Actual Total Load', linestyle='dashdot',color='yellow')
        plt.plot(time, mean_spec, label='Mean of Day-ahead Total Load Forecast', linestyle='--',color='green')

        ax.bar(time - width, real, width, color='b', label='Actual Total Load', align='edge')
        ax.bar(time, spec, width, color='r', label='Day-ahead Total Load Forecast', align='edge')
        ax.xaxis.set_major_locator(loc)
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')

        plt.tight_layout()
        plt.legend()
        plt.show()

    # A graph of the normal distribution of the Actual Load
    def normal_distribution(self,real,mean_real):
        import scipy.stats
        value=real[:]
        value.sort()
        x_min = 0
        x_max = value[-1]+value[0]
        mean = mean_real
        std = statistics.stdev(real)
        x = np.linspace(x_min, x_max,)

        y = scipy.stats.norm.pdf(x, mean, std)

        plt.plot(x, y, color='black',linewidth='2')

        # ----------------------------------------------------------------------------------------#
        # fill area 1

        pt1 = mean + std
        plt.plot([pt1, pt1], [0.0, scipy.stats.norm.pdf(pt1, mean, std)], color='black')

        pt2 = mean - std
        plt.plot([pt2, pt2], [0.0, scipy.stats.norm.pdf(pt2, mean, std)], color='black')

        ptx = np.linspace(pt1, pt2, 10)
        pty = scipy.stats.norm.pdf(ptx, mean, std)

        plt.fill_between(ptx, pty, color='#0b559f', alpha=1)

        # ----------------------------------------------------------------------------------------#
        # fill area 2

        pt1 = mean + std
        plt.plot([pt1, pt1], [0.0, scipy.stats.norm.pdf(pt1, mean, std)], linestyle='dashdot',color='red')

        pt2 = mean + 2.0 * std
        plt.plot([pt2, pt2], [0.0, scipy.stats.norm.pdf(pt2, mean, std)], linestyle='dashdot',color='red')

        ptx = np.linspace(pt1, pt2, 10)
        pty = scipy.stats.norm.pdf(ptx, mean, std)

        plt.fill_between(ptx, pty, color='#2b7bba', alpha=1)

        # ----------------------------------------------------------------------------------------#
        # fill area 3

        pt1 = mean - std
        plt.plot([pt1, pt1], [0.0, scipy.stats.norm.pdf(pt1, mean, std)], linestyle='dashdot',color='red')

        pt2 = mean - 2.0 * std
        plt.plot([pt2, pt2], [0.0, scipy.stats.norm.pdf(pt2, mean, std)], linestyle='dashdot',color='red')

        ptx = np.linspace(pt1, pt2, 10)
        pty = scipy.stats.norm.pdf(ptx, mean, std)

        plt.fill_between(ptx, pty, color='#2b7bba', alpha=1)

        # ----------------------------------------------------------------------------------------#
        # fill area 4

        pt1 = mean + 2.0 * std
        plt.plot([pt1, pt1], [0.0, scipy.stats.norm.pdf(pt1, mean, std)], linestyle='dashdot',color='red')

        pt2 = mean + 3.0 * std
        plt.plot([pt2, pt2], [0.0, scipy.stats.norm.pdf(pt2, mean, std)], linestyle='dashdot',color='red')

        ptx = np.linspace(pt1, pt2, 10)
        pty = scipy.stats.norm.pdf(ptx, mean, std)

        plt.fill_between(ptx, pty, color='#539ecd', alpha=1)

        # ----------------------------------------------------------------------------------------#
        # fill area 5

        pt1 = mean - 2.0 * std
        plt.plot([pt1, pt1], [0.0, scipy.stats.norm.pdf(pt1, mean, std)], linestyle='dashdot',color='red')

        pt2 = mean - 3.0 * std
        plt.plot([pt2, pt2], [0.0, scipy.stats.norm.pdf(pt2, mean, std)], linestyle='dashdot',color='red')

        ptx = np.linspace(pt1, pt2, 10)
        pty = scipy.stats.norm.pdf(ptx, mean, std)

        plt.fill_between(ptx, pty, color='#539ecd', alpha=1)

        # ----------------------------------------------------------------------------------------#
        # fill area 6

        pt1 = mean + 3.0 * std
        plt.plot([pt1, pt1], [0.0, scipy.stats.norm.pdf(pt1, mean, std)], linestyle='dashdot',color='red')

        pt2 = mean + 10.0 * std
        plt.plot([pt2, pt2], [0.0, scipy.stats.norm.pdf(pt2, mean, std)], linestyle='dashdot',color='red')

        ptx = np.linspace(pt1, pt2, 10)
        pty = scipy.stats.norm.pdf(ptx, mean, std)

        plt.fill_between(ptx, pty, color='#89bedc', alpha=1)

        # ----------------------------------------------------------------------------------------#
        # fill area 7

        pt1 = mean - 3.0 * std
        plt.plot([pt1, pt1], [0.0, scipy.stats.norm.pdf(pt1, mean, std)], linestyle='dashdot',color='red')

        pt2 = mean - 10.0 * std
        plt.plot([pt2, pt2], [0.0, scipy.stats.norm.pdf(pt2, mean, std)], linestyle='dashdot',color='red')

        ptx = np.linspace(pt1, pt2, 10)
        pty = scipy.stats.norm.pdf(ptx, mean, std)

        plt.fill_between(ptx, pty, color='#89bedc', alpha=1)

        # ----------------------------------------------------------------------------------------#

        plt.grid()


        plt.title('Normal distribution of Actual Load', fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})

        plt.xlabel('LOAD [MW]',fontdict={'fontname' : 'Times New Roman', 'fontsize': 10})
        plt.ylabel('Normal Distribution',fontdict={'fontname' : 'Times New Roman', 'fontsize': 10})
        plt.show()

class Second():

    def __init__(self,number):
        total=[]
        self.num=number
        #import all the dates and separate the Actual from the forecast
        for i in range(self.num):
            #import a date
            list,dates=scanner()
            a=find_date(dates)
            print(f'The day is a {a}')
            print_values(list)
            #add the name
            total.append(dates +' which is a ' + a)
            # add the Real Actual Load
            total.append(get_real(list))
            # add the Day-Ahead Forecast Actual Load
            total.append(get_spec(list))
        while(True):
            print("Please enter a number from 1 to 5:\n1: The Mean value of the Actual Total Load.")
            print("2: The Mean Absolute Error of all the dates in order.")
            print("3: The Mean Absolute Percentage % Error of all the dates in order.")
            print("4: The Standard Deviation of all the dates in order.")
            print("5: The Mean Squared Error of all the dates in order.")
            print("6: A Graph of all the Actual Total Load of all the dates.")
            print("7: A Graph of the Percentage % of Error of all the dates.")
            print("8: A Graph of the Percentage % of Accuracy of all the dates")
            print("9: A Graph of Load per hour as a percentage % of maximum daily energy load ")
            print("To end the program just enter 'End' or 'Telos'.")
            scan = input("Please enter your choice: ")
            print('\n')
            if scan=='1':
                self.mean_value_2(total)
            elif(scan=='2'):
                self.MAE(total)
            elif(scan=='3'):
                self.MAPE(total)
            elif(scan=='4'):
                self.standard_deviation(total)
            elif(scan=='5'):
                self.meansquarederror(total)
            elif(scan=='6'):
                self.graph_2(total)
            elif(scan=='7'):
                self.percent_error_2(total)
            elif(scan=='8'):
                self.percent_accuracy_2(total)
            elif(scan=='9'):
                self.percent_peak_energy_2(total)
            elif(scan.lower()=="end" or scan.lower()=="telos"):
                break
            else:
                print("Something went wrong\n")
                pass

    # Find the Mean Average Percentage Error of all the dates in ascending order
    def mean_value_2(self,total):
        dict = OrderedDict()
        for i in range(0, len(total), 3):
            a = round(statistics.mean(total[i + 1]),3)
            dict[total[i]] = a

        d = OrderedDict(sorted(dict.items(), key=itemgetter(1)))
        print("\nThe Mean Actual Load in ascending order:")

        for key, value in d.items():
            print(f'\tOn {key} the Mean Total Load is {value} MW')
        print('\n')

    #Find the Mean Average Percentage Error of all the dates in ascending order
    def MAPE(self,total):
        dict = OrderedDict()
        for i in range(0, len(total), 3):
            a = round(err(total[i+1],total[i+2])*100,3)
            dict[total[i]] = a

        d = OrderedDict(sorted(dict.items(), key=itemgetter(1)))
        print("\nThe Mean Absolute percentage % Error in ascending order:")

        for key, value in d.items():
            print(f'\tOn {key} the Mean Absolute percentage Error is {value}%')
        print('\n')

    #Find the Mean Average Error of all the dates in ascending order
    def MAE(self,total):
        dict = OrderedDict()

        for i in range(0, len(total), 3):
            a = round(mae(total[i+1],total[i+2]),3)
            dict[total[i]] = a

        d = OrderedDict(sorted(dict.items(), key=itemgetter(1)))
        print("\nThe Mean Absolute Error in ascending order:")

        for key, value in d.items():
            print(f'\tOn {key} the Mean Absolute Error is {value} MW')
        print('\n')

    #Find the Standard Deviation of all the dates in ascending order
    def standard_deviation(self,total):
        dict = OrderedDict()

        for i in range(0, len(total), 3):
            a = round(statistics.stdev(total[i+1]),3)
            dict[total[i]] = a

        d = OrderedDict(sorted(dict.items(), key=itemgetter(1)))
        print("\nThe Standard Deviation in ascending order:")

        for key, value in d.items():
            print(f'\tOn {key} the Standard Deviation Error is {value}')
        print('\n')

    #Find the Mean Squared Error of all the dates in ascending order
    def meansquarederror(self,total):
        dict = OrderedDict()

        for i in range(0, len(total), 3):
            a = round(mean_squared_error(total[i+1],total[i+2]), 3)
            dict[total[i]] = a

        d = OrderedDict(sorted(dict.items(), key=itemgetter(1)))
        print("\nThe Mean Squared Error in ascending order:")

        for key, value in d.items():
            print(f'\tOn {key} the Mean Squared Error is {value}')
        print('\n')

    #Graph the Actual Load of all the dates
    def graph_2(self,total):
        loc = plticker.MultipleLocator(base=1.0)
        values=['-', '--', '-.', ':', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted']
        cycol=cycle(values)
        time=[x for x in range(24)]
        plt.figure(figsize=(10, 4))
        list_1=[]
        for i in range(0, len(total), 3):
            a = round(statistics.mean(total[i + 1]),3)
            list_1.append([a]*len(total[1]))
        j=0
        for i in range(0,len(total),3):
            plt.plot(time,total[i+1],label=total[i],c=(random.random(),random.random(),random.random()),linewidth='2',marker='.',markersize='10',markeredgecolor='black')
            plt.plot(time, list_1[j], label="The mean of "+ total[i], linestyle=next(cycol), c=(random.random(),random.random(),random.random()))
            j+=1

        plt.title("Graph of all the Actual Loads",fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Load [MW]',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()
        plt.show()

    # A graph of the percentage of error of all the Actual Loads
    def percent_error_2(self,total):
        loc = plticker.MultipleLocator(base=1.0)
        time=[x for x in range(24)]
        plt.figure(figsize=(10, 4))
        list_1=[]
        for i in range(0, len(total), 3):
            a= percent_error(total[i+1],total[i+2])
            list_1.append(a)
        j=0
        for i in range(0,len(total),3):
            plt.plot(time,list_1[j],label=total[i],c=(random.random(),random.random(),random.random()),linewidth='2',marker='.',markersize='10',markeredgecolor='black')
            j+=1
        plt.title("The percentage % of Error of all the dates",fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Error %',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()
        plt.show()

    # A graph of the percentage of accuracy of all the Actual Loads
    def percent_accuracy_2(self,total):
        loc = plticker.MultipleLocator(base=1.0)
        time=[x for x in range(24)]
        plt.figure(figsize=(10, 4))
        list_1=[]
        for i in range(0, len(total), 3):
            a= [100-abs(x) for x in percent_error(total[i+1],total[i+2])]
            list_1.append(a)

        j=0
        for i in range(0,len(total),3):
            plt.plot(time,list_1[j],label=total[i],c=(random.random(),random.random(),random.random()),linewidth='2',marker='.',markersize='10',markeredgecolor='black')
            j+=1
        plt.title("The percentage % of Accuracy of all the dates",fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Accuracy %',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()
        plt.show()

    # A graph of the Actual Loads as a percentage of max Load of the Given Day
    def percent_peak_energy_2(self,total):
        loc = plticker.MultipleLocator(base=1.0)
        time=[x for x in range(24)]
        plt.figure(figsize=(10, 4))
        list_1=[]
        for i in range(0, len(total), 3):
            b=[(x/max(total[i+1]))*100 for x in total[i+1]]
            list_1.append(b)
        j=0
        for i in range(0,len(total),3):
            plt.plot(time,list_1[j],label=total[i],c=(random.random(),random.random(),random.random()),linewidth='2',marker='.',markersize='10',markeredgecolor='black')
            j+=1
        plt.title("Load per hour as a percentage % of maximum daily energy load",fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Load as a %',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()
        plt.show()

class Third():
    def __init__(self):
        #Add the date
        list, dates = scanner()
        day, month, year = dates.split('.')
        day_name = date(int(year), int(month), int(day))
        print(f'The day is a {day_name.strftime("%A")}')
        print("The Load of GREECE is:")
        #import for Greece
        print_values(list)
        real_gre = get_real(list)
        spec_gre = get_spec(list)
        mean_real_gre = [statistics.mean(real_gre)] * len(real_gre)
        error_gre = percent_error(real_gre, spec_gre)
        # Choose a foreign country and Import the Actual and Forecast values
        while (True):
            print("Please choose one of the following countries: France,Finland,Czechia,Poland,Portugal,Spain")
            a=input("Choice: ")
            try:
                country= a.upper()
            except:
                country='FALSE'
            if(country=="FRANCE"):
                list_for=self.load_fra(dates)
                population=65408602
                gdp_2019=2715518
                gdp= self.gdp_adjustor(year,gdp_2019,1.7)
                break
            elif(country=="FINLAND"):
                list_for=self.load_fin(dates)
                population=5548732
                gdp_2019=269296
                gdp= self.gdp_adjustor(year,gdp_2019,2.1)
                break
            elif(country=="CZECHIA"):
                list_for=self.load_cze(dates)
                population=10727551
                gdp_2019=250681
                gdp= self.gdp_adjustor(year,gdp_2019,3.2)
                break
            elif(country=="POLAND"):
                list_for=self.load_pol(dates)
                population=37808065
                gdp_2019=595858
                print(gdp_2019)
                gdp= self.gdp_adjustor(year,gdp_2019,4.5)
                print(gdp)
                break
            elif(country=="PORTUGAL"):
                list_for=self.load_por(dates)
                population=10169149
                gdp_2019=238785
                gdp= self.gdp_adjustor(year,gdp_2019,2.65)
                break
            elif(country=="SPAIN"):
                list_for=self.load_spa(dates)
                population=46771662
                gdp_2019=1393491
                gdp= self.gdp_adjustor(year,gdp_2019,2.6)
                break
            else:
                print("Please enter the country's name properly.")
        print(f'\nThe Load of {country} is:')
        print_values(list_for)
        # find the Actual Load
        real_for = get_real(list_for)
        # find the Day-Ahead Forecast Load
        spec_for = get_spec(list_for)
        # find the Mean Value of the Actual Load
        mean_real_for = [statistics.mean(real_for)] * len(real_for)
        error_for = percent_error(real_for, spec_for)
        while(True):
            print(f"\nPlease enter a number from 1 to 10:\n1: A line graph the Actual load Values of GREECE and {country}.")
            print(f"2: A bar chart the Actual load Values of GREECE and {country}.")
            print(f"3: A line graph of the % of error of GREECE and {country}.")
            print(f"4: A line graph of the % of accuracy of GREECE and {country}.")
            print(f"5: A line graph of load per hour as a percentage of maximum daily energy load of GREECE and {country}.")
            print(f"6: Print the Mean Absolute Error of GREECE and {country}.")
            print(f"7: Print the Mean Absolute Percentage Error of GREECE and {country}.")
            print(f"8: Print the Standard Deviation of the Actual Load of GREECE and {country}")
            print(f"9: Print the Mean Squared Error of GREECE and {country}")
            print(f"10: Print the Mean value of the Actual Load of GREECE and {country}.")
            print(f"11: A line graph of the per capita power consumption/Actual Load of GREECE and {country}")
            print(f"12: A line graph of the Actual Load per GDP(Nominal) GREECE and {country}")

            print("To end the program just enter 'End' or 'Telos'.")
            choice=input("Please enter your choice: ")
            print("\n")
            if(choice=='1'):
                self.graph_power_compare(real_gre, real_for, mean_real_gre, mean_real_for,country)
            elif(choice=='2'):
                self.bar_chart_both_compare(real_gre, real_for, mean_real_gre, mean_real_for,country)
            elif(choice=='3'):
                self.percent_error_compare(error_gre,error_for,country)
            elif (choice == '4'):
                self.percent_accuracy_compare(error_gre,error_for,country)
            elif (choice == '5'):
                self.peak_energy_load_compare(real_gre,real_for,country)
            elif (choice == '6'):
                print(f'The Mean Absolute Error of GREECE is: {round(mae(real_gre, spec_gre), 3)} MW')
                print(f'The Mean Absolute Error of {country} is: {round(mae(real_for, spec_for), 3)} MW')
            elif (choice == '7'):
                print(f'The Mean Absolute Percentage % Error of GREECE is: {round(err(real_gre, spec_gre) * 100, 3)}%')
                print(f'The Mean Absolute Percentage % Error of {country} is: {round(err(real_for, spec_for) * 100, 3)}%')
            elif (choice == '8'):
                print(f'The Standard Deviation of the Actual Load of GREECE is: {round(statistics.stdev(real_gre), 3)}')
                print(f'The Standard Deviation of the Actual Load of {country} is: {round(statistics.stdev(real_for), 3)}')
            elif (choice == '9'):
                print(f'The Mean Squared Error of GREECE is: {round(mean_squared_error(real_gre, spec_gre), 3)}')
                print(f'The Mean Squared Error of {country} is: {round(mean_squared_error(real_for, spec_for), 3)}')
            elif (choice == '10'):
                print(f'The Mean value of the Actual Load of GREECE is: {round(statistics.mean(real_gre), 3)} MW')
                print(f'The Mean value of the Actual Load of {country} is: {round(statistics.mean(real_for), 3)} MW')
            elif(choice=='11'):
                self.per_capita_power(real_gre, mean_real_gre, real_for, mean_real_for, country, population)
            elif(choice=='12'):
                self.load_per_gdp(real_gre, mean_real_gre, real_for, mean_real_for, country, gdp, year)
            elif (choice.lower() == "end" or choice.lower() == "telos"):
                break
            else:
                print("Something went wrong\n")
                pass

    #A bar chart of the load as a percentage of the Peak Load for both countries
    def bar_chart_both_compare(self,real_gre, real_for, mean_real_gre, mean_real_for,country):
        loc = plticker.MultipleLocator(base=1.0)
        time = [x for x in range(24)]
        width = np.min(np.diff(time)) / 3
        fig = plt.figure(figsize=(10, 4))
        ax = fig.add_subplot(111)

        plt.plot(time, mean_real_gre, label='Mean of Actual Total Load of GREECE', linestyle='dashdot', color='yellow')
        plt.plot(time, mean_real_for, label=f'Mean of Actual Total Load of {country}', linestyle='--', color='green')
        plt.title(f"Actual Load Greece vs {country}",fontdict={'fontname': 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Load [MW]', fontdict={'fontname': 'Times New Roman', 'fontsize': 10})
        plt.xlabel('Time [HOURS]', fontdict={'fontname': 'Times New Roman', 'fontsize': 10})

        ax.bar(time - width, real_gre, width, color='b', label='Actual Total Load of GREECE', align='edge')
        ax.bar(time, real_for, width, color='r', label=f'Actual Total Load of {country}', align='edge')
        ax.xaxis.set_major_locator(loc)
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')

        plt.tight_layout()
        plt.savefig('Forecast and Real bar.png')
        plt.legend()
        plt.show()

    # A graph of the Load of both countries
    def graph_power_compare(self,real_gre, real_for, mean_real_gre, mean_real_for,country):
        loc = plticker.MultipleLocator(base=1.0)
        time = [x for x in range(24)]
        plt.figure(figsize=(10, 4))
        plt.plot(time, mean_real_gre, label='Mean of Actual Total Load of GREECE', linestyle='dashdot', color='yellow')
        plt.plot(time, mean_real_for, label=f'Mean of Actual Total Load of {country}', linestyle='--', color='green')
        plt.plot(time, real_gre, label='Actual Total Load of Greece', color='blue', linewidth='2', marker='.', markersize='10',markeredgecolor='black', markerfacecolor='blue')
        plt.plot(time, real_for, label=f'Mean of Actual Total Load of {country} ', color='red', linewidth='2', marker='.', markersize='10',markeredgecolor='black', markerfacecolor='red')
        plt.title(f"Actual Total Load [GREECE] vs [{country}]",fontdict={'fontname': 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Load [MW]', fontdict={'fontname': 'Times New Roman', 'fontsize': 10})
        plt.xlabel('Time [HOURS]', fontdict={'fontname': 'Times New Roman', 'fontsize': 10})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()
        plt.show()

    # A graph of the load as a percentage of the Peak Load for both countries
    def peak_energy_load_compare(self,real_gre,real_for,country):
        loc = plticker.MultipleLocator(base=1.0)

        maximum = real_gre.index(max(real_gre))
        list_gre = []
        for i in real_gre:
            list_gre.append(round((i / real_gre[maximum]) * 100, 3))
        list_for = []
        maximum = real_for.index(max(real_for))

        for i in real_for:
            list_for.append(round((i / real_for[maximum]) * 100, 3))

        time = [x for x in range(24)]
        plt.figure(figsize=(10, 4))
        plt.plot(time, list_gre, label='Value percent % of GREECE', color='blue', linewidth='2', marker='.', markersize='10',markeredgecolor='black', markerfacecolor='blue')
        plt.plot(time, list_for, label=f'Value percent % of {country}', color='Red', linewidth='2', marker='.', markersize='10',markeredgecolor='black', markerfacecolor='red')

        plt.title("Load per hour as a percentage of maximum daily energy load ",fontdict={'fontname': 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Load %', fontdict={'fontname': 'Times New Roman'})
        plt.xlabel('Time [HOURS]', fontdict={'fontname': 'Times New Roman'})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()
        plt.show()

    # Load the dates for the different countries
    def load_fra(self,date):
        a=f'https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime={date}+00:00|CET|DAY&biddingZone.values=CTY|10YFR-RTE------C!BZN|10YFR-RTE------C&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)'
        html_text=requests.get(a).text
        soup= BeautifulSoup(html_text,'lxml')
        data=soup.find_all('td',class_="dv-value-cell")
        list_1=[]
        for i in data:
            list_1.append(i.text)
        return list_1

    def load_fin(self,date):
        a=f'https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime={date}+00:00|EET|DAY&biddingZone.values=CTY|10YFI-1--------U!BZN|10YFI-1--------U&dateTime.timezone=EET_EEST&dateTime.timezone_input=EET+(UTC+2)+/+EEST+(UTC+3)'
        html_text=requests.get(a).text
        soup= BeautifulSoup(html_text,'lxml')
        data=soup.find_all('td',class_="dv-value-cell")
        list_1=[]
        for i in data:
            list_1.append(i.text)
        return list_1

    def load_pol(self,date):
        a=f'https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime={date}+00:00|CET|DAY&biddingZone.values=CTY|10YPL-AREA-----S!BZN|10YPL-AREA-----S&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)'
        html_text=requests.get(a).text
        soup= BeautifulSoup(html_text,'lxml')
        data=soup.find_all('td',class_="dv-value-cell")
        list_1=[]
        for i in data:
            list_1.append(i.text)
        return list_1

    def load_cze(self,date):
        a=f'https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime={date}+00:00|CET|DAY&biddingZone.values=CTY|10YCZ-CEPS-----N!BZN|10YCZ-CEPS-----N&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)'
        html_text=requests.get(a).text
        soup= BeautifulSoup(html_text,'lxml')
        data=soup.find_all('td',class_="dv-value-cell")
        list_1=[]
        for i in data:
            list_1.append(i.text)
        return list_1

    def load_por(self,date):
        a=f'https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime={date}+00:00|WET|DAY&biddingZone.values=CTY|10YPT-REN------W!BZN|10YPT-REN------W&dateTime.timezone=WET_WEST&dateTime.timezone_input=WET+(UTC)+/+WEST+(UTC+1)'
        html_text=requests.get(a).text
        soup= BeautifulSoup(html_text,'lxml')
        data=soup.find_all('td',class_="dv-value-cell")
        list_1=[]
        for i in data:
            list_1.append(i.text)
        return list_1

    def load_spa(self,date):
        a=f'https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime={date}+00:00|CET|DAY&biddingZone.values=CTY|10YES-REE------0!BZN|10YES-REE------0&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)'
        html_text=requests.get(a).text
        soup= BeautifulSoup(html_text,'lxml')
        data=soup.find_all('td',class_="dv-value-cell")
        list_1=[]
        for i in data:
            list_1.append(i.text)
        return list_1

    # A graph of the percentage of Error for the 2 countries
    def percent_error_compare(self,error_gre,error_for,country):
            loc = plticker.MultipleLocator(base=1.0)
            time=[x for x in range(24)]
            plt.figure(figsize=(10,4))
            plt.plot(time,error_gre,label='Error of Greece',color='blue',linewidth='2',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='blue')
            plt.plot(time,error_for,label=f'Error of {country}',color='red',linewidth='2',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='red')
            plt.title(f"How off was the Forecast? [GREECE] VS [{country}]",fontdict={'fontname' : 'Times New Roman', 'fontsize': 16})
            plt.ylabel('Error %',fontdict={'fontname' : 'Times New Roman'})
            plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman'})
            plt.xticks([x for x in range(24)])
            plt.ylim(-20, 20)

            ax = plt.gca()
            ax.tick_params(axis='x', colors='blue')
            ax.tick_params(axis='y', colors='red')
            ax.xaxis.set_major_locator(loc)

            plt.tight_layout()
            plt.legend()
            plt.show()

    # A graph of the percent accuracy for the 2 countries
    def percent_accuracy_compare(self,error_gre,error_for,country):
            accuracy_gre=[]
            for i in error_gre:
                accuracy_gre.append(100-abs(i))
            accuracy_for = []
            for i in error_for:
                accuracy_for.append(100 - abs(i))

            time=[x for x in range(24)]
            loc = plticker.MultipleLocator(base=1.0)
            plt.figure(figsize=(10,4))
            plt.plot(time,accuracy_gre,label='Accuracy of the Forecest in GREECE',color='blue',linewidth='2',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='blue')
            plt.plot(time,accuracy_for,label=f'Accuracy of the Forecest in {country}',color='red',linewidth='2',marker='.',markersize='10',markeredgecolor='black',markerfacecolor='red')

            plt.title(f"How close was the Forecast? [GREECE] vs [{country}]",fontdict={'fontname' : 'Times New Roman', 'fontsize': 20})
            plt.ylabel('ACCURACY %',fontdict={'fontname' : 'Times New Roman','fontsize': 10})
            plt.xlabel('Time [HOURS]',fontdict={'fontname' : 'Times New Roman'})
            plt.xticks([x for x in range(24)])

            ax = plt.gca()
            ax.tick_params(axis='x', colors='blue')
            ax.tick_params(axis='y', colors='red')
            ax.xaxis.set_major_locator(loc)

            plt.tight_layout()
            plt.legend()
            plt.show()

    # A graph of the per capita Load of the 2 countries
    def per_capita_power(self,real_gre,mean_real_gre,real_for,mean_real_for,country,pop):
        loc = plticker.MultipleLocator(base=1.0)
        time = [x for x in range(24)]
        list_gre=[]
        for i in real_gre:
            list_gre.append(1000000*(i/10375594))
        list_for=[]
        for i in real_for:
            list_for.append(1000000*(i/pop))
        list_mean_gre=[1000000*(x/10375594) for x in mean_real_gre]
        list_mean_for=[1000000*(x/pop) for x in mean_real_for]
        plt.figure(figsize=(10, 4))
        plt.plot(time, list_mean_gre, label='Mean Load per capita GREECE', linestyle='dashdot', color='yellow')
        plt.plot(time, list_mean_for, label=f'Mean Load per capita {country}', linestyle='--', color='green')
        plt.plot(time, list_gre, label='Power per capita GREECE', color='blue', linewidth='2', marker='.', markersize='10',markeredgecolor='black', markerfacecolor='blue')
        plt.plot(time, list_for, label=f'Power per capita {country}', color='red', linewidth='2', marker='.', markersize='10',markeredgecolor='black', markerfacecolor='red')
        plt.title(f"Actual Total Load per capita [GREECE] vs [{country}]",fontdict={'fontname': 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Load [W]', fontdict={'fontname': 'Times New Roman', 'fontsize': 10})
        plt.xlabel('Time [HOURS]', fontdict={'fontname': 'Times New Roman', 'fontsize': 10})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()
        plt.show()

    #A graph of the Load as a percentage of GDP
    def load_per_gdp(self,real_gre,mean_real_gre,real_for,mean_real_for,country,gdp,year):
        loc = plticker.MultipleLocator(base=1.0)
        time = [x for x in range(24)]
        gdp_gre= self.gdp_adjustor(int(year),209853,2)
        list_gre=[]
        for i in real_gre:
            list_gre.append(i/gdp_gre)
        list_for=[]
        for i in real_for:
            list_for.append((i/gdp))
        list_mean_gre=[(x/gdp_gre) for x in mean_real_gre]
        list_mean_for=[(x/gdp) for x in mean_real_for]
        plt.figure(figsize=(10, 4))
        plt.plot(time, list_mean_gre, label='Mean Load per G.D.P. GREECE', linestyle='dashdot', color='yellow')
        plt.plot(time, list_mean_for, label=f'Mean Load per G.D.P. {country}', linestyle='--', color='green')
        plt.plot(time, list_gre, label='Load per G.D.P. GREECE', color='blue', linewidth='2', marker='.', markersize='10',markeredgecolor='black', markerfacecolor='blue')
        plt.plot(time, list_for, label=f'Load per G.D.P. {country}', color='red', linewidth='2', marker='.', markersize='10',markeredgecolor='black', markerfacecolor='red')
        plt.title(f"Actual Load per Nominal G.D.P.(World Bank) in USD [GREECE] vs [{country}]",fontdict={'fontname': 'Times New Roman', 'fontsize': 20})
        plt.ylabel('Load/G.D.P [MW/$]', fontdict={'fontname': 'Times New Roman', 'fontsize': 10})
        plt.xlabel('Time [HOURS]', fontdict={'fontname': 'Times New Roman', 'fontsize': 10})
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.xaxis.set_major_locator(loc)
        plt.tight_layout()
        plt.legend()
        plt.show()

    # Adjust the 2019 GDP World Bank Estimates by the growth
    def gdp_adjustor(self,year,gdp_2019,growth):
        time=2019-int(year)
        if(time<0):
            gdp = gdp_2019 * (((1 + ((growth / 100.0))) ** abs(time)))
        elif(time==0):
            return gdp_2019
        else:
            gdp = gdp_2019 * (((1 - ((growth / 100.0) )) ** abs(time)))
        return gdp

if __name__ == '__main__':
    main()
