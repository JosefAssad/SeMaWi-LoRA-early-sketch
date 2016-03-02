THIS CODE IS FOR ILLUSTRATION ONLY. IT IS FULL OF GAPS, INCONSISTENCIES, AND IT DOES NOT MANDATE ANY PARTICULAR SOLUTION STRUCTURE. IT IS INTENDED ONLY TO ILLUSTRATE THE NOTION OF SMALL SINGLE PURPOSE PYTHON CLASSES FACILITATING THE INTEGRATION OF DANISH PUBLIC SECTOR SYSTEMS, WITH LoRA IN THE HEART AND RABBITMQ FOR TRANSPORT

# PyLoRa

PyLoRa is a Python API which speaks with the ReST interface exposed by a LoRa service. LoRa exposes a ReST interface implementing the OIO standard. This standard is large; the following is currently implemented in PyLoRa:

- Bruger and related subtypes (e.g. Virkning)

This implementation aims for compatibility with the LoRa ReST service first and foremost. In the event that the LoRa service disagrees with the standard, the LoRa implementation is respected.

# Hacking on PyLoRa

PyLoRa development occurs in a virtualenv. The included file requirements.txt is to be used to install the python modules PyLoRa requires in the virtualenv.

PyLoRa depends on the following python modules:

* IPython

# Implementation notes:

LoRa is an implementation of [this](http://digitaliser.dk/resource/991439/artefact/Informations-+og+meddelelsesmodeller+for+Organisation+%5bvs.+1.1%5d.pdf) standard.

PyLoRa follows the LoRa implementation of the OIO standard, as the name suggests.

## Differences between the standard and the implementation

In the OIO standard (in the linked PDF), a BrugerRegistrering does not appear to have an attribute "fratidspunkt". such an attribute is returned from the LoRa JSON API when returning an object organisation/bruger. Currently, this extraneous element is ignored by PyLoRa.

The LoRa organisation/bruger JSON responses contain further elements not seen in the linked OIO standard: 'note', and 'livscykluskode'. PyLoRa implements these elements.

# The dime tour

This code is intended to paint a picture rather than for actual use in real world code. As such, this section points out the relevant bits. don't worry, there isn't a lot of code.

Relevant bits:

1. note the instantiation in client.py of a lora object and a semawi object.
2. Note how the semawi object has a method indicating lora-awareness; this method pulls it systems from lora into a semawi template.
3. It doesn't use rabbitmq. I did say the code is not complete. :)
4. Note, separate module for python OIO objects. No serious dependencies, very stark python classes. The more stark, the more reusable in contexts we cannot predict.
5. Technically, this code actually works for very limited definitions of the word "works". do not assume it does however.
