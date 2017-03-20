# str-macros

A minimalistic python package allowing to define macros on string based class attributes

## Installation

This package does not have any dependencies and works just fine with
Python 2.7 and Python 3.5+.

To install it via **pip** just run the following command:

```
pip install str-macros
```

## Slow start

The basic idea of this project is to provide a tool for simple macros execution.

For better understanding, let's start with an example.

Let's imagine that you are a developer who creates a tool for
a convenient work with Google AdWords. 

Let's define two classes AdBanner and AdCampaign:

```python

class AdCampaign(object):
    def __init__(self, campaign_id, name):
        self.campaign_id = campaign_id
        self.name = name

class AdBanner(object):
    def __init__(self, ad_id, name, url, campaign):
        self.ad_id = ad_id
        self.name = name
        self.url = url
        self.campaign = campaign
```

But one important condition is that we want to have some analytics
about user clicks on our banners. To achieve this, we use utm labels and we want banner
urls to be in the following format: 

```http://test.com/?utm_ad_name=test_ad&utm_campaign=test_campaign```

So, when we create an ad we specify not real url, but an url with some
macros like this:


```python
campaign = AdCampaign(1, 'test campaign')
banner = AdBanner(
    id=1,
    name='banner [banner_id] for campaign [campaign_name] [random]',
    url='http://test.ru/?utm_id=[banner_id]',
    campaign=campaign
)
```
So, we have four macros here:
```[banner_id], [campaign_name], [banner_id], [random]``` and we
want to enable them when we create it and send info to Google.

## Usage

Let's see how to deal with it:

```python
import random

from str_macros import MacrosMixin


class AdBanner(MacrosMixin):
    MACRO_FIELDS = (
        'name', 'url'
    )
    
    MACRO_MAP = {
        'banner_id': lambda self: str(self.ad_id),
        'campaign_id': lambda self: str(self.campaign.id),
        'campaign_name': lambda self: self.campaign.name,
        'random': lambda self: str(random.randint(1, 100)),
    }

    def __init__(self, ad_id, name, url, campaign):
        self.ad_id = ad_id
        self.name = name
        self.url = url
        self.campaign = campaign
```

OK, now we have for variables which can be used in fields (attributes) which
are defined in MACRO_FIELDS and MACRO_MAP: macros that should be executed
for each of the variables.

#### Important params:
- MACRO_FIELDS: tuple or list of attributes in which to look
for patterns
- MACRO_MAP: dict {'pattern': func}: what function to run when a pattern found.
Should take only one argument - current object (self).
 In this dictionary, keys are patterns, but without [].

When you assign some initial values to str fields - pattern shoud
be inside of **[]**.


Attention: if in MACRO_MAP you specify a function which uses a
field which is specified in MACRO_FIELDS you are going to end up
in an infinite recursion, so - don't make such mistakes. Example of such mistage:

```python
MACRO_FIELDS = (
    'name', 'url'
)
MACRO_MAP = {
    'banner_name': lambda self: self.name
    # Danger!
    # if you have pattern [banner_name] in name - infinite recursion
}
 ```

### Basic usage

By default, macros are disabled. So:

```python
campaign = AdCampaign(1, 'test campaign')
banner = AdBanner(
    id=1,
    name='banner [banner_id] for campaign [campaign_name] [random]',
    url='http://test.ru/?utm_id=[banner_id]',
    campaign=campaign
)

print(banner.name)
# Macros disabled now
# banner [banner_id] for campaign [campaign_name] [random]'
AdBanner.start_macros()

# Macros enabled now
print(AdBanner.is_macros_enabled()) # True
print(banner.name)
# banner 1 for campaign test campaign 5

AdBanner.stop_macros()
print(banner.name)
# And disabled again
# banner [banner_id] for campaign [campaign_name] [random]'
print(AdBanner.is_macros_enabled()) # False
```

### Using context manager
```python
from str_macros import enabled_macros


AdBanner.is_macros_enabled() # False
with enabled_macros(AdBanner):
    # macros are enabled here
    AdBanner.is_macros_enabled() # True
# and here they are already disabled
```

### Using decorator
```python
from str_macros import enable_macros

@enable_macros(AdBanner)
def send_data():
    # macros are enabled here
    pass

```

## Django

This package works just fine with Django models CharFields and has been
developed mostly for it.

## Author

Dmitry Abramov &copy;