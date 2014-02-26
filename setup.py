from distutils.core import setup 

setup(
    name = "ComplexNetworkSim",
    version = "0.1.3",
    author = "Joe Schaul",
    author_email = "joe.schaul@gmail.com",
    description = "Simulation framework for agents connected in a (complex) network.",
    keywords = "networks, simulation, complex networks, discrete event simulation, temporal complex networks",	
    license = "freeBSD",    
	url = "http://complexnetworksim.0sites.net/", 
    packages = ['ComplexNetworkSim', 'ComplexNetworkSim.unittests'], 
	requires = ['networkx', 'simpy', 'matplotlib'],
	install_requires = ['networkx', 'simpy'],
    long_description = open('README.txt').read(),
    classifiers = [
        "Development Status :: 3 - Alpha",
		"License :: OSI Approved :: BSD License",	 
		"Intended Audience :: Developers",
		"Intended Audience :: Science/Research",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Topic :: Scientific/Engineering"
		
    ],
)
