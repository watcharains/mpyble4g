from max1704x import max17043

m = max17043()


#print(i2c.scan())

# read and print the voltage of the battery
print(m.getVCell())
print(m.inAlert())
