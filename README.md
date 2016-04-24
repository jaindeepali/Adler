### Adler

Ready-to-use text classification corpus generation from [TechTC-300 Test Collection](http://techtc.cs.technion.ac.il/techtc300/techtc300.html) . The final dataset uses chi-squared feature selection and tf-idf feature weighting. Classification is done using a [Decision-Jungle classifier in AzureML](http://gallery.cortanaintelligence.com/Experiment/de2c89307d8849feb90c1de6ccdeffdd) .

### Setup

* Clone the repo: `git clone https://github.com/jaindeepali/Adler`
* Create config file from sample: `cp Adler/config/sample.config.json Adler/config/config.json`
* Open config.json and edit the path to the data directory
* Create python virtual environment: `virtualenv .venv`
* Activate virtual environment: `source .venv/bin/activate`
* Install Adler package: `python setup.py install`
* Run script to generate dataset: `/scripts/generate.py`
