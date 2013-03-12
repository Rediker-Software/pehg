=========================
Getting started with Pehg
=========================

Pehg is a simple application that can be used to generate easy to use APIs for Django.

------------
Installation
------------

Pehg was designed to be as simple as possible to install and use.  To install it, all you need to do is download the source and run the installer.

~~~~~~~~~~~~
Dependencies
~~~~~~~~~~~~

Pehg only has a few dependencies that you need to watch for.  There are only two dependencies that are not optional:

* Django 1.3 - 1.5
* Python 2.5 - 2.7

Pehg may work on other configurations, but it is only tested on the above ones.  There are some other dependencies that while they are not required, are recommended to install:

* simplejson
   While Pehg works with the default JSON libraries, simplejson is required for Python 2.5  It is recommended over the default JSON library as it works considerably faster.
* pyyaml
   The YAML serializer depends on pyyaml to serialize and unserialize the data.

~~~~~~~~~~~~~~~~~~~~~~
Install Pehg using Pip
~~~~~~~~~~~~~~~~~~~~~~

At the moment, Pehg is not available on Pip.  You can still install Pehg using pip with the tarball that is available through GitHub.::

   pip install https://github.com/kevin-brown/django-pehg/archive/master.tar.gz#egg=pehg

~~~~~~~~~~~~~~~~~~~~~
Install Pehg from Git
~~~~~~~~~~~~~~~~~~~~~

You can build and install Pehg from the source that is available on GitHub.::

   git clone https://github.com/kevin-brown/django-pehg.git pehg
   cd pehg
   python setup.py install

This will clone the Pehg repository on GitHub and run the installer which is included with pehg.

------------------
Setting up the API
------------------

We recommend placing the components for your API in a file called api.py in your application folder, but you can place them anywhere in your project.  Pehg provides a simple method of versioning using the Resource object.::

   # app/api.py
   from pehg.resources import ModelResource
   from .models import Apple
   
   class AppleResource(ModelResource):
        model = Apple
        resource_name = "apple"

In this example we are using a ModelResource that is attached to an Apple model.  Apple is a simple model with a few fields which aren't as important, the Resource will be set up to match the fields on the Model.

Pehg also comes with an Api object which can be used to manage multiple resources at once.::

   # app/urls.py
   from django.conf.urls import patterns, url
   from pehg.api import Api
   from .api import AppleResource
   
   api = new Api()
   api.register_resource(AppleResource())
   
   urlpatterns = patterns("",
       url(r"api/", include(api.urls),
       url(r"apples/", includes(AppleResource().urls)),
   )

You can use the Api objects to combine mutliple resources under one roof (in this example we are only using the single AppleResource) or you can hook up individular resources to your urlconf.  This gives you the flexibility of determining where you want certain resources to be accessed from.

After adding the urls to the urlconf, quite a few new urls are avaialble to you:

* http://localhost:8000/api/v1/
* http://localhost:8000/api/v1/apple.json
* http://localhost:8000/api/v1/apple.xml
* http://localhost:8000/api/v1/apple/
