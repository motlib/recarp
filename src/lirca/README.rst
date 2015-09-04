How to decode an AC IR remote protocol using Ipython
====================================================

Setup
-----
Raspberry PI with...

* IR receiver connected
* LIRC installed and set up
* Network connection

Remote PC with...

* Python 3	
* Ipython installed (try qtconsole as well)
* Matplotlib setup (to use %pylab in the interactive console)

Record IR Signals
-----------------
First of all there is the boring part. Getting the raw data. Because the 
IR receiver is connected to the Raspberry PI there is a convenience
method to remotely capture the lirc timings. 

.. code-block:: python
	raw = lirca.read_raw_from_ssh('192.168.1.53', 'pi', 'password')

	Press any key to stop capturing: 

Now press a key on the remote and press enter to receive the stdout from the
Raspberry.

My remote's OFF command:::

	Out[1155]: '  4400840\n\n     3429     1511      550      276      536      234\n      581     1110      516      237      578     1057\n      577      233      575      241      601      222\n      612     1026      577     1050      572      238\n      576      235      578      238      574     1060\n      578     1051      578      240      585      228\n      575      240      586      227      582      236\n      598      215      599      213      565      261\n      535      294      507      307      492      329\n      485      359      449      334      477     1157\n      476      363      436      364      445      392\n      434      366      431      403      407      391\n      409      400      413     1223      407      403\n      425      394      409      408      417      403\n      410     1220      412      401      421      391\n      412      399      415      430      386      401\n      413      410      412     1223      408      400\n      411     1218      440     1195      412     1215\n      414     1211      417     1220      441     1190\n      412

Now let's write the raw timings in a file and name it clearly. When using 
Ipython it's helpful to create yourself a short temporary function to 
write the content:

.. code-block::http://sphinx.pocoo.org/markup/code.html#line-numbers
	def write(fname, string):
		with open(fname, 'w') as fh:
			fh.write(string)

Save all your files to folder only containing the lirc raw fihttp://sphinx.pocoo.org/markup/code.html#line-numbersles:::
	write('./data/off', raw)

Now repeat this for all kinds of commands:http://sphinx.pocoo.org/markup/code.html#line-numbershttp://sphinx.pocoo.org/markup/code.html#line-numbers

	In [1164]: ls
	off_19C_auto_auto  on_20C_auto_medium      on_23C_auto_auto
	off_20C_auto_auto  on_20C_auto_mute        on_24C_auto_auto
	off_24C_auto_auto  on_20C_blowing_auto     on_25C_auto_auto
	on_18C_auto_auto   on_20C_cool_auto        on_30C_auto_auto
	on_19C_auto_auto   on_20C_dehumidify_auto  up_24C_auto_auto
	on_20C_auto_auto   on_20C_heating_auto     up_25C_auto_auto
	on_20C_auto_high   on_21C_auto_auto
	on_20C_auto_low    on_22C_auto_aut

When you have a certain amount of files to compare we can start to analyse
them. I wrote a class `RawTimings` that runs some analyse methods on the
data. Lets' start with creating the objects for each raw file:

	timings = lirca.RawTimings.from_folder('./data')

	Out[11]: 
	{'off_19C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b21e3048>,
	 'off_20C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b2250898>,
	 'off_24C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b2250208>,
	 'on_18C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b2250a90>,
	 'on_19C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b2250dd8>,
	 'on_20C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b2250780>,
	 'on_20C_auto_high': <lirca.raw.RawTimings at 0x7fe2b2250668>,
	 'on_20C_auto_low': <lirca.raw.RawTimings at 0x7fe2b2250ba8>,
	 'on_20C_auto_medium': <lirca.raw.RawTimings at 0x7fe2b21e3390>,
	 'on_20C_auto_mute': <lirca.raw.RawTimings at 0x7fe2b2250550>,
	 'on_20C_blowing_auto': <lirca.raw.RawTimings at 0x7fe2b21e3160>,
	 'on_20C_cool_auto': <lirca.raw.RawTimings at 0x7fe2b2277f28>,
	 'on_20C_dehumidify_auto': <lirca.raw.RawTimings at 0x7fe2b22509b0>,
	 'on_20C_heating_auto': <lirca.raw.RawTimings at 0x7fe2b2250320>,
	 'on_21C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b21e3278>,
	 'on_22C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b22500f0>,
	 'on_23C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b2250438>,
	 'on_24C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b2250ef0>,
	 'on_25C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b21e2f98>,
	 'on_30C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b2250cc0>,
	 'up_24C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b21e2e80>,
	 'up_25C_auto_auto': <lirca.raw.RawTimings at 0x7fe2b21e34a8>

Now we have a dictionary with the filenames as keys and `RawTimings`
instances as objects. Before we now start to analyze the data some backeground
to the data itself. The LIRC raw timing format is just a sequence of on and off
times of the (modulated) IR signal:

	pi@ultraRASPI1 ~ $ mode2 -r -d /dev/lirc0 
	space 1540892	# time elapsed from start of receiving to first signal
	pulse 3429		# ON
	space 1469		# OFF
	pulse 576		# ON
	...

This raw data now is stored in the `RawTimings` objects.




