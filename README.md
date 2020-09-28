# yfs
Yahoo Finance Scraper

A Yahoo Finance Scraper with a WYSIWYG approach.

The goal of this api is to get out of the users way and not make any assumptions on how they will be using the data. I tried to make things as close as possible to the yahoo finance website.

Just extract and clean the data. The goal is to stay lite and out of your way.

Serialize the data to json, dict or a 2D pandas dataframe.

Every Function which downloads data can accept a proxy to ensure data is downloaded in its entirety.

In fact you can install the requests-whaor which supplies a rotating proxy to bypass rate limits..

## Features
* Company/Symbol lookup
* Summary Page
* Option Chains
* Statistics Page

## TODO/ Future Features - in order of precedence
* [ ] More testing
* [ ] Docs
* [ ] Profile Page
* [ ] Financials
* [ ] Analysis
* [ ] Holders
* [ ] Sustainability
* [ ] Historical Page
* [ ] Chart Page
* [ ] Conversations Page maybe ¯\_(ツ)_/¯
