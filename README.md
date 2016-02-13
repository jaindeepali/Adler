### Adler

Ready-to-use text classification corpus generation from [TechTC-300 Test Collection](http://techtc.cs.technion.ac.il/techtc300/techtc100.html) .

### Setup

* Clone the repo: `git clone https://github.com/jaindeepali/Adler`
* Create config file from sample: `cp Adler/config/sample.config.json Adler/config/config.json`
* Open config.json and edit the path to the data directory
* Create python virtual environment: `virtualenv .venv`
* Activate virtual environment: `source .venv/bin/activate`
* Install Adler package: `python setup.py install`
* Run script to generate dataset: `/scripts/generate.py`