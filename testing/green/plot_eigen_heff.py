import pylab as py


m = py.genfromtxt("eigen_heff.dat").transpose() # read the file

x = m[0]

fig = py.figure() # create figure
fig.subplots_adjust(0.2,0.2)
fig.set_facecolor("white")
spall = fig.add_subplot(111)

for i in range(1,len(m)/2):
  spall.plot(x,m[i*2+1],marker="o",linestyle="-",c="red",linewidth=4.0)
#  spall.plot(x,m[i*2+1],marker="o",linestyle="None",c="red",linewidth=4.0)
#  spall.set_xlabel("$\phi/2\pi$",size=30)
  spall.set_xlabel("$\Delta$",size=30)
#  spall.set_xlabel("$\mu$",size=30)
  spall.set_ylabel("Energy",size=30)
#  spall.set_xlim([0.0,2.0])
py.show()

