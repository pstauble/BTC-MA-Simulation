import requests
import time
import sys


btcwallet=0
loopvar=0 #Must be set at zero as it is the variable to count number of loops
executions=30 #How many times the full function repeats.
sleeptime=30 #length of pauses between each full loop.
loop_pause=30 #Length of the pause between each time the calculate function runs.
prices_sum=5 #How many prices in the average.
buffer=0.4 #How much above the trend price does recent price need to be before it buys.
ema_sum=0

# Set all variables to zero so we can get a working average.
ema_sum=0
price1=0
price2=0
price3=0
price4=0
price5=0

def get_price():
	try:
		price=float(requests.post("https://api.kraken.com/0/public/Ticker", data={'pair':"XXBTZEUR"}).json()["result"]["XXBTZEUR"]["c"][0])
		return price
	except:
		time.sleep(20)
		print "Error has occurred. Getting price again..."
		price=float(requests.post("https://api.kraken.com/0/public/Ticker", data={'pair':"XXBTZEUR"}).json()["result"]["XXBTZEUR"]["c"][0])
		
		
	
	
def krakentime():
	time= requests.get("https://api.kraken.com/0/public/Time")
	return time.json()['result']['rfc1123']
	
def calculation():
		global btcwallet
		global eurwallet
		global ema_sum
		global price1,price2,price3,price4,price5
		global loop_pause

		if btcwallet<=0 and eurwallet<=0:
			#Check if you have any money left before continuing the simulation.
			print "You have no BTC or EUR left. The simulation is over."
			sys.exit(0)
		else:
			pass

		trend=ema_sum/40 #Calculate the trend value.
		
		localtime=time.strftime("%H:%M:%S") #Get the time
		price=get_price() #Get the actual price.
		
		try:
			trend_data=open("trend_data.txt","a")
			price_data=open("price_data.txt","a")
			price_data.write(str(price)+",")
			trend_data.write(str(trend)+",")
			trend_data.close()
			price_data.close()
		except:
			pass
		
		localtime=time.strftime("%H:%M:%S")
		
		print "Trend price is: " + str(trend) +" EUR at %r" %localtime
		print "BTC Price: " + str(price) + " EUR. Wallet contains: %r EUR. Time: %r"%(eurwallet, localtime)
		
		try:
			if price==0 or price1==0 or price2==0 or price3==0 or price4==0 or price5==0: #Loop must run fully once to get a working moving average.
				print "Warming up..."
			
			elif price>(trend*1.005) and eurwallet>0:
				btcwallet=round((eurwallet*.9965)/price,8)
				eurwallet=0
				print "************ BUY: %r  BTC at %r EUR at %r." %(btcwallet, price, localtime)
				
			elif price<trend and btcwallet>0:
				eurwallet=round((btcwallet*price)*.9965,2)
				btcwallet=0
				print "************ SELL: BTC sold at %r EUR for %r EUR at %r." %(price,eurwallet,localtime)
			
			else:
				localtime=time.strftime("%H:%M:%S")
				print "Loop run, no change at %r."	%localtime
		except: 
			pass
		
	

	
def purchase(i):
	global eurwallet
	global btcwallet
	global ema_sum
	global price1,price2,price3,price4,price5
	loop_pause=i
	print "*"*50
	print "*"*50
	print "*"*50
	walletfile=open("wallet.txt","r")
	eurwallet=float(walletfile.read())
	eurwallet=round(eurwallet,2)
	walletfile.close()
	

	
	
	
	localtime=time.strftime("%H:%M:%S")
	print "Welcome Patrick. The simulation will now begin at %r." %localtime
	timer=raw_input("How many minutes would you like to run the simulation? ")
	max_time=60*int(timer)
	start_time=time.time()

	
	print "It will run for %r minutes and will start at %r." %(timer, localtime)



	print "Function initialising..."
	
	while (time.time() - start_time) < max_time:

		
		#Here is the EMA part that makes it different from MA
		
		######################################### Loop1
		try:
			price1=get_price()
			ema_sum=10*price1+6*price2+7*price3+8*price4+9*price5
			time.sleep(loop_pause)

		
			calculation()
			time.sleep(loop_pause)
		except:
			pass
		########################### Loop2
		try:
			price2=get_price()
			ema_sum=9*price1+10*price2+6*price3+7*price4+8*price5
			time.sleep(loop_pause)

			calculation()
			time.sleep(loop_pause)
		except:
			pass
		################################ Loop3
		try:
			price3=get_price()
			ema_sum=8*price1+9*price2+10*price3+6*price4+7*price5
			time.sleep(loop_pause)

			calculation()
			time.sleep(loop_pause)
		except:
			pass
		#####################3Loop4
		try:
			price4=get_price()
			ema_sum=7*price1+8*price2+9*price3+10*price4+6*price5
			time.sleep(loop_pause)
			
			calculation()
			time.sleep(loop_pause)
		except:
			pass		
		###################### Loop5	
		try:
			price5=get_price()
			ema_sum=6*price1+7*price2+8*price3+9*price4+10*price5
			time.sleep(loop_pause)
			
			calculation()
			time.sleep(loop_pause)
		except:
			pass	
	if btcwallet>0:
		eurwallet=price*btcwallet
		btcwallet=0
		eurwallet=round(eurwallet,2)
	else:
		pass
	print "The simulation is complete. You now have %r EUR."%eurwallet
	walletfile=open("wallet.txt","w")
	walletfile.truncate()
	walletfile.write(str(eurwallet))
	
purchase(30)