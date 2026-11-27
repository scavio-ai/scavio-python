# Scavio Python SDK

[![PyPI version](https://img.shields.io/pypi/v/scavio.svg)](https://pypi.org/project/scavio/)
[![Downloads](https://img.shields.io/pypi/dm/scavio.svg)](https://pypi.org/project/scavio/)
[![Python](https://img.shields.io/pypi/pyversions/scavio.svg)](https://pypi.org/project/scavio/)
[![Tests](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml/badge.svg)](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The official Python SDK for the [Scavio](https://scavio.dev?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) Search API. Access real-time data from 174 sources -- Google, ChatGPT, Gemini, Amazon, Walmart, Costco, Best Buy, TCGplayer, the Nintendo eShop, H&M, Zara, Uniqlo, ASOS, Fashion Nova, Vinted, Mercari, Depop, Poshmark, OfferUp, thredUP, Macy's, Saks Fifth Avenue, Kohl's, JCPenney, Belk, Dick's Sporting Goods, Academy Sports + Outdoors, REI, L.L.Bean, Foot Locker, Zappos, 6pm, Fanatics, Gap, Old Navy, Banana Republic, Athleta, Abercrombie & Fitch, Hollister, Bath & Body Works, Williams Sonoma, Pottery Barn, West Elm, Bed Bath & Beyond, QVC, HSN, Argos, Media Expert, Action, HEMA, Nordstrom, Nordstrom Rack, Lowe's, Sam's Club, BJ's Wholesale Club, Canadian Tire, SportChek, Mark's, RONA, Dollar General, Dollar Tree, Discount Tire, Sephora, Ulta Beauty, Dermstore, Space NK, Lookfantastic, Cult Beauty, YesStyle, Notino, Douglas, Boots, ALDI, Micro Center, Newegg, Sweetwater, Walgreens, CVS, Whole Foods Market, Harbor Freight, AutoZone, O'Reilly Auto Parts, RockAuto, Cars.com, Autotrader, CarGurus, CarMax, Carvana, TrueCar, Edmunds, Kelley Blue Book, Bring a Trailer, Ace Hardware, Tractor Supply, Michaels, Nike, Staples, Instacart, PC Express, PetSmart, Petco, iHerb, Chewy, Menards, HEB, Kroger, Publix, IKEA, Wayfair, Ashley Furniture, Maisons du Monde, Carrefour, Allegro, bol.com, OLX, Trendyol, Spec's, Decathlon, Mercado Libre, KaBuM!, Magazine Luiza, Casas Bahia, Extra, Ponto, Buscape, Zoom, Drogasil, Droga Raia, Leroy Merlin, Natura, O Boticario, Eudora, Centauro, eBay, EstateSales.net, Rakuten, Target, Home Depot, YouTube, Reddit, X, TikTok, TikTok Shop, Instagram, LinkedIn, Threads, Kuaishou, Zillow, Redfin, Realtor.com, Rightmove, Trulia, StreetEasy, Rent.com, Apartment Guide, RentCafe, Movoto, HotPads, Apartment List, Compass, AffordableHousing.com, Lennar, Extra Space Storage, Public Storage, U-Haul, Booking.com, Tripadvisor, Airbnb, Vrbo, Expedia, Yelp, Indeed, Glassdoor, the Apple App Store, Google Play, SEC EDGAR, Companies House, G2, Capterra, Trustpilot, Reclame Aqui, Goodreads, Barnes & Noble, ThriftBooks, Google Ads Transparency and the Meta Ad Library -- plus `extract` for reading any URL and for mapping, crawling or batch-extracting whole websites, and `company.enrich` for a business's emails, phones, socials and owner from its website or a Google Maps place_id, all with a single API key. Built for AI agents, LLM applications, and data pipelines.

> One API key, 60 data sources, 355 endpoints, structured JSON with knowledge graphs. A powerful alternative to Tavily, SerpAPI, and ScraperAPI for developers who need more than just web search.

## Why Scavio

| Feature | Scavio | Tavily | SerpAPI | ScraperAPI |
|---------|--------|--------|---------|------------|
| Google Search | Yes | Yes | Yes | Yes |
| ChatGPT and Gemini Answers with Cited Sources | Yes | No | No | No |
| Amazon Products | Yes | No | Yes | No |
| Walmart Products | Yes | No | No | No |
| Costco Warehouse Prices, Stock, Gas and Coupons (13 endpoints) | Yes | No | No | No |
| BJ's Wholesale Club Prices, Sale Dates, Member-Only Price Flags, Coupons, Reviews, Categories and the Club Directory (US; 7 endpoints) | Yes | No | No | No |
| Store-Level Prices and Stock (Lowe's, Sam's Club, Canadian Tire, Dollar General; 21 endpoints) | Yes | No | No | No |
| SportChek and Mark's Prices in CAD with the Was Price, Sale Label and Sale End Date, Sizes and Colours with Assigned-Store Units, SportChek Reviews, Mark's Questions, L'Equipeur in French (Canada; 16 endpoints) | Yes | No | No | No |
| RONA Store Prices in CAD for Up to 60 Articles at One Store with Exact Units, Search, Category and Weekly Deals Priced at a Chosen Store, Sale End Text, 403 Stores, Stock Near a Store (Canada; 9 endpoints) | Yes | No | No | No |
| PC Express Grocery Prices in CAD at Each Banner's Default Store (Real Canadian Superstore, No Frills, Loblaws, Maxi and 6 more), Deal End Dates, PC Optimum Offers, Unit Prices, Product Nutrition, Pickup Stores (Canada; 7 endpoints) | Yes | No | No | No |
| Beauty, Pharmacy, Grocery and Electronics Stores (Sephora, Ulta Beauty, ALDI, Micro Center, Walgreens, CVS; Sephora Canada CAD Prices, Sale Prices, Dated Offers and Stores; 26 endpoints) | Yes | No | No | No |
| Grocery, Pet, Supplement and Hardware Stores (Whole Foods Market, Harbor Freight, PetSmart, Petco, iHerb, Chewy, Menards; 33 endpoints) | Yes | No | No | No |
| Nordstrom Products, Reviews, Categories, Brands, Store Pickup and Store Locator (8 endpoints) | Yes | No | No | No |
| Nordstrom Rack Clearance, Flash Events, Products, Reviews, Store Pickup and Store Locator (8 endpoints) | Yes | No | No | No |
| Best Buy Products, Open-Box Prices, Store Pickup, Deal of the Day, Reviews and Batch Prices; Best Buy Canada Exact Units per Store, EHF by Province, Sale End Dates and Questions (10 endpoints) | Yes | No | No | No |
| Newegg Prices, Every Seller's Offer by Condition, Reviews, Deals and Marketplace Seller Stores (US, Canada and 9 Global storefronts; 10 endpoints) | Yes | No | No | No |
| Sweetwater Music Gear Prices, Price Drops and Rebates, Units on Hand and on Order, Serial-Numbered Units with Weights, Reviews and the Deal Zone (US; 6 endpoints) | Yes | No | No | No |
| TCGplayer Card Market Prices, Price History, Recent Sales, Listings, Set Price Guides and Sellers (13 endpoints) | Yes | No | No | No |
| Nintendo eShop Prices by Country, Sale End Dates, Deals, Releases and DLC (46 countries; 6 endpoints) | Yes | No | No | No |
| H&M Prices by Country, Member Prices, Online Stock by Size, Stores and Production (47 countries; 9 endpoints) | Yes | No | No | No |
| Zara Prices by Country, Online and Store Stock by Size, Materials, Special Prices and Stores (102 storefronts; 12 endpoints) | Yes | No | No | No |
| Uniqlo Prices by Country, Online and Store Stock by Size, Reviews with Fit and Limited Offers (41 markets; 12 endpoints) | Yes | No | No | No |
| ASOS Prices by Country and Currency, Online Stock by Size, Reviews by Store, Sale and New In (235 countries; 11 endpoints) | Yes | No | No | No |
| Fashion Nova Sale Prices, Compare-At Prices, Sizes in Stock and Reviews (104 countries; 7 endpoints) | Yes | No | No | No |
| Vinted Listings, Prices, Sellers, Brands and Categories across 27 country sites (9 endpoints) | Yes | No | No | No |
| Mercari Sold Prices, Listings, Items, Brands, Trending and Japan Sellers (US and Japan; 11 endpoints) | Yes | No | No | No |
| Depop Listings by Buyer Market, Shop Sold Prices, Shop Profiles and Reviews (9 markets; 14 endpoints) | Yes | No | No | No |
| Poshmark Sold Prices, Listings, Closets and Love Notes (US and Canada; 15 endpoints) | Yes | No | No | No |
| OfferUp Asking Prices Around Any US ZIP, the Same Item in Different Metros, Cars and Trucks by Dealer or Private Seller, Make, Year and Mileage, Listings with Condition and Vehicle Details, Seller Profiles (US; 5 endpoints) | Yes | No | No | No |
| thredUP Prices, Estimated Retail, Sold Listings and Deals (US store; 12 endpoints) | Yes | No | No | No |
| Macy's Products, Prices, Deals, Reviews, Brand Pages and Store Pickup (9 endpoints) | Yes | No | No | No |
| Gap, Old Navy, Banana Republic and Athleta Prices, Promotion and Markdown Prices, Batch Prices, In, Low or Out Store Stock by Size, Stores and Deals (US and Canada; 11 endpoints) | Yes | No | No | No |
| Abercrombie & Fitch, abercrombie kids, Hollister and Gilly Hicks Prices by Storefront, Promotions, Exact Store Units per SKU, Stores and Reviews (16 storefronts; 10 endpoints) | Yes | No | No | No |
| Bath & Body Works Prices, Product Promotions with Dates, Current Offers, Store Pickup Purchase Limits, Stores and Review Summaries (US and Canada; 10 endpoints) | Yes | No | No | No |
| Williams Sonoma, Pottery Barn and West Elm Prices, Online Stock Ranges, Delivery Dates, Store Pickup, Floor Samples, Stores and Categories (7 brands, US and Canada; 12 endpoints) | Yes | No | No | No |
| Bed Bath & Beyond Sale and Compare Prices, Sale End Dates, Exact Online Stock per Option, Delivery Estimates, Reviews, Q&A and Stores (US; 9 endpoints) | Yes | No | No | No |
| QVC and HSN Prices, Special Prices, Today's Special, On Air Now, Program Guide, Recently Aired Items and Reviews (QVC US, UK, DE, IT, JP; HSN US; 10 endpoints) | Yes | No | No | No |
| Saks Fifth Avenue Designer Sale Prices, Products, Stock, Designer Pages and Store Pickup (9 endpoints) | Yes | No | No | No |
| Kohl's Clearance, Sale Prices, Kohl's Cash, Coupon Codes and Store Pickup Units (9 endpoints) | Yes | No | No | No |
| Belk Sale Prices, Belk Rewards+ Tier Prices, Coupons with Belk's Own After-Code Price, Doorbusters, Exact Store Units and Reviews (US; 10 endpoints) | Yes | No | No | No |
| Rakuten Cash Back Rates and Was Rates by Store, Rate Checks for 100 Stores, Store Coupons, Event Deals and In-Store Offers (US, UK and Canada; 9 endpoints) | Yes | No | No | No |
| JCPenney Clearance, Sale Prices, Coupon Codes, Store Unit Counts, Reviews and Q&A (11 endpoints) | Yes | No | No | No |
| Dick's Sporting Goods Clearance, Per-Size Prices, Store Unit Counts and Reviews (9 endpoints) | Yes | No | No | No |
| Academy Sports + Outdoors Prices, Was Prices and Deals, Exact Units per Store for Pickup, Stores and Categories (US; 9 endpoints) | Yes | No | No | No |
| REI Prices, Sale, Clearance and Outlet Deals, Store Pickup Status near a ZIP, Reviews and Stores (US; 9 endpoints) | Yes | No | No | No |
| L.L.Bean Prices and Sale Prices (US, Canada and 12 Countries), Exact Store Units per SKU, Reviews with Fit Data, Delivery Estimates and Deals (11 endpoints) | Yes | No | No | No |
| Foot Locker Release Calendar, Size Availability, Sale Prices, Reviews and Q&A (13 markets; 10 endpoints) | Yes | No | No | No |
| Zappos and 6pm Prices, Exact Warehouse Units per Size, Width and Color, Reviews with Fit Ratings, Questions and Lowest Prices (US; 7 endpoints) | Yes | No | No | No |
| Fanatics Merchandise: Jersey Sale, Clearance and With-Code Prices, Size Stock Levels, League Stores and Reviews (8 markets; 5 endpoints) | Yes | No | No | No |
| Argos Store Stock by UK Postcode, Prices, Was Prices, Badges and Reviews (UK; 10 endpoints) | Yes | No | No | No |
| Media Expert Black Week Prices, Omnibus 30-Day Low, Code Prices, Store Stock and Reviews (Poland; 13 endpoints) | Yes | No | No | No |
| Action Weekly Deals, Prices by Country, Stores, Opening Hours and Reviews (19 storefronts in 16 countries; 16 endpoints) | Yes | No | No | No |
| HEMA Store Stock by City or Postcode, Dated Promotions, Prices by Market and Reviews (Netherlands, Belgium, France, Germany; stores also Luxembourg and Austria; 13 endpoints) | Yes | No | No | No |
| AutoZone Parts Prices by Vehicle, Core Charges, Warranty, Part-Number Cross-Reference, Reviews and Stores (US; Brazil search, product and store stock; 12 endpoints) | Yes | No | No | No |
| O'Reilly Auto Parts Part-Number Cross-Reference with Prices, Core Charges, Rebates, Store Stock near a ZIP and VIN Decode (US; Mexico store directory; 14 endpoints) | Yes | No | No | No |
| RockAuto Parts Prices by Vehicle (Make, Year, Model, Engine), Every Brand and Tier, Core Charges, Part-Number Search, 15 Display Currencies (11 endpoints) | Yes | No | No | No |
| Cars.com New and Used Listings near a ZIP, Deal Labels, Dealers, Dealer Inventory and Reviews, Model Reviews, Research (US; 8 endpoints) | Yes | No | No | No |
| Autotrader Listings near a ZIP, Deal Labels, KBB Fair Price Range, Price History, Dealers and Makes (US; 5 endpoints) | Yes | No | No | No |
| CarGurus Listings with Expected Price and Deal Rating, Dealer Inventory, Price Trends, Research and Expert Reviews (US, Canada, UK; 8 endpoints) | Yes | No | No | No |
| CarMax No-Haggle Prices near a ZIP, Price Drops, Shipping Fees, 263 Stores and Store Inventory, Owner Reviews, Recent CarMax Offers per Model Year (12 endpoints) | Yes | No | No | No |
| Carvana Used-Car Prices, KBB Values, Shipping Costs and Labels by Make and Model, Inspection and Imperfections, Model-Year Guides and Trims (US; 6 endpoints) | Yes | No | No | No |
| TrueCar New and Used Prices near a ZIP, Price Rating, Dealer Fees, National Price and Trim Stats, Model Overviews and Owner Reviews (US; 9 endpoints) | Yes | No | No | No |
| Edmunds Listings with Deal Rating, MSRP, Invoice and Edmunds Suggested Price per Trim, Appraisal Values per Condition, Owner Reviews (US; 8 endpoints) | Yes | No | No | No |
| Kelley Blue Book Car Values (Fair Purchase Price, Private Party, Trade-In, Auction; 17 Price Types) at a ZIP, Listings with KBB Fair Price, Owner Reviews, Dealers (US; 8 endpoints) | Yes | No | No | No |
| Ace Hardware Prices by Store, Exact Units on Hand at a Store and Its 25 Nearest, Weekly Ad per Store, Deals and Paint Colors (US; 11 endpoints) | Yes | No | No | No |
| Tractor Supply Prices by Store and Price Zone, One Item at 25 Stores, Exact Store Stock with In-Transit Units, Fulfillment and Promotions (US; 12 endpoints) | Yes | No | No | No |
| Michaels Craft Prices with Reg. Price and Offer Dates, Exact Units at the Stores near a ZIP, One Store's Inventory, Variants and Deals (US; Canada in English or French; 11 endpoints) | Yes | No | No | No |
| Nike Sale Prices with Full Price and Discount, Every Size with GTIN, Release Calendar with Per-Size Levels, Same Style Code Across Markets (62 storefronts in 42 countries; 8 endpoints) | Yes | No | No | No |
| Staples Ink and Paper Prices with Staples' Own Price per Unit and Cost per Page, Promotions with Expiry, Units at the Stores near a ZIP, Reviews and Q&A (US; Canada search and product in English or French; 12 endpoints) | Yes | No | No | No |
| Dollar Tree Case Prices next to Unit Prices, Case Packs, Minimum Order and Split Cases, Units at a Store and Its Nearby Stores, Stores and Reviews (US; Canada store pages; 10 endpoints) | Yes | No | No | No |
| Discount Tire Tire Prices by Store, the Same Tire at Other Discount Tire and America's Tire Stores, Tires That Fit a Vehicle, Exact Units at the Stores near a ZIP, Reviews (US; 15 endpoints) | Yes | No | No | No |
| Vevor Prices per Storefront in 13 Countries, Was Price Only During a Deal with Deal Dates, Variants with Their Own Price and Stock, Shipping Fee by State or Province, the Same SKU on Every Storefront, Reviews (13 storefronts; 11 endpoints) | Yes | No | No | No |
| Nellis Auction Lot Prices: Current Bid, Bid Count and Nellis's Estimated Retail Price, a Sold Lot's Final Price, Bid History Without Bidder Names, Pickup Warehouses and Hours (6 US shopping locations; 4 endpoints) | Yes | No | No | No |
| EstateSales.net Estate Sales near a ZIP with Dates and Picture Counts, Sale Details, Companies by Metro, Marketplace Items (US; 6 endpoints) | Yes | No | No | No |
| Bring a Trailer Auction Results, Sale Prices and High Bids, Model Price History with Sell-Through Rate, Listings with Bids and Comments, Live Auctions (8 endpoints) | Yes | No | No | No |
| Dermstore Skincare Prices, RRP and Dermstore's Offer Text per Product and Brand, Variants with Their Own Price and Stock, UPC, Current Offers with End Times, US vs Canada Prices, the 10 Latest Reviews (US and Canada; 7 endpoints) | Yes | No | No | No |
| Space NK Luxury Beauty Prices in GBP, EUR and AUD, Discount and Promo Badges, Online Stock per Shade, Reviews, UK Store Availability and Gifts with Purchase (4 markets; 9 endpoints) | Yes | No | No | No |
| Lookfantastic Beauty Prices, RRP and Offer Text on 10 Country Sites in 22 Currencies, Variants with Their Own Price and Stock, Barcodes, Voucher Codes with End Times (7 endpoints) | Yes | No | No | No |
| Cult Beauty Prices, RRP and Offer Text in 12 Currencies, Variants with Their Own Price and Stock, Barcodes, Voucher Codes with End Times (7 endpoints) | Yes | No | No | No |
| YesStyle Asian Beauty Prices per Shipping Country (39 Countries), Deal Lists, Sale End Dates, Shades and Sizes, Reviews with Star Summary (9 endpoints) | Yes | No | No | No |
| Notino Perfume and Cosmetics Prices on 27 Storefronts in Their Own Currencies, 30-Day Lowest Price, EAN per Variant, Reviews, Stores (10 endpoints) | Yes | No | No | No |
| Douglas Beauty Prices, Was Price, RRP and 30-Day Lowest Price on 15 Storefronts, Deals, Stores with Hours, Review Summary (10 endpoints) | Yes | No | No | No |
| Boots Prices, Was Price, Saving, Unit Price and Offers, Store Availability near a UK Postcode, Stores and Store Hours (UK and Ireland; 4 endpoints) | Yes | No | No | No |
| Instacart Prices by Store at a ZIP, Price Compare Across Every Store, Delivery vs In-Store Prices, Deals and Reviews (US; Canada in English or French; 11 endpoints) | Yes | No | No | No |
| Carrefour Grocery Prices by Store, Promotions, Nutri-Score, Stores and Fuel Prices (France, Argentina, Romania, Belgium; 9 endpoints) | Yes | No | No | No |
| Allegro Offers, Every Seller's Price, Sellers, Sold Counts and Auctions (Poland, Czechia, Slovakia, Hungary; 7 endpoints) | Yes | No | No | No |
| bol.com Buy Box, Lowest-Priced Seller Offers, EAN Lookup, Seller Ratings and Deals (Netherlands and Belgium; 9 endpoints) | Yes | No | No | No |
| OLX Europe Classifieds: Listings, Ads, Sellers, Category Filters and Similar Ads (7 markets; 9 endpoints) | Yes | No | No | No |
| Trendyol Seller Prices, Buy Box, Reviews, Q&A, Coupons and Rankings (35 markets; 12 endpoints) | Yes | No | No | No |
| Trustpilot Businesses and Reviews (6 endpoints) | Yes | No | No | No |
| Reclame Aqui Company Reputation, Complaints, Rankings and Segments (Brazil; 8 endpoints) | Yes | No | No | No |
| Goodreads Book Ratings and Rating Distribution, Reader Reviews by Star and Language, Authors, Series, Editions, Lists, Quotes and New Releases (14 endpoints) | Yes | No | No | No |
| Barnes & Noble Book Prices and Formats by EAN or ISBN, Bestseller Lists, Store Pickup Flags, Stores, Collections and Deals (US; 10 endpoints) | Yes | No | No | No |
| ThriftBooks Used Book Prices per Format and Condition, ISBN Lookup, Editions, Copies for Sale and Reviews (US; 8 endpoints) | Yes | No | No | No |
| Mercado Libre Listings, Reviews and Best Sellers (MX, BR, AR, CO; 5 endpoints) | Yes | No | No | No |
| KaBuM! Card and Pix Prices, Offers with Units Left, Marketplace Sellers, Shipping by CEP and Reviews (Brazil; 7 endpoints) | Yes | No | No | No |
| Magazine Luiza Prices, Pix Prices, Coupons, Deal End Times, Reviews and Stores (Brazil; 8 endpoints) | Yes | No | No | No |
| Casas Bahia, Extra and Ponto Products with Every Seller's Price, Pix Price and Installments (Brazil; 4 endpoints) | Yes | No | No | No |
| Buscape and Zoom Store Offers, Daily Lowest Price History, Store Coupons and Shipping Estimates (Brazil; 12 endpoints) | Yes | No | No | No |
| Drogasil and Droga Raia Prices, Deals, Coupons, Store Pickup and Stores (Brazil; 11 endpoints) | Yes | No | No | No |
| Leroy Merlin Prices in 7 Markets, Brazil Regional Prices and Exact Store Units, Reviews and Stores (13 endpoints) | Yes | No | No | No |
| Natura Beauty Prices, Shades and Black Friday Deals in 6 Latin American Markets, Brazil Stores (7 endpoints) | Yes | No | No | No |
| O Boticario and Eudora Card and Pix Prices, Shades, Reviews, Promotions and Store Pickup (Brazil; 11 endpoints) | Yes | No | No | No |
| Centauro Sporting Goods Prices per Size, Freight and Store Pickup by CEP (Brazil; 7 endpoints) | Yes | No | No | No |
| YouTube Search | Yes | No | Yes | No |
| Reddit Data (12 endpoints) | Yes | No | No | No |
| X Data (11 endpoints) | Yes | No | No | No |
| TikTok Data (24 endpoints) | Yes | No | No | No |
| TikTok Shop Data (8 endpoints) | Yes | No | No | No |
| Instagram Data (20 endpoints) | Yes | No | No | No |
| LinkedIn Data (9 endpoints) | Yes | No | No | No |
| eBay Sold-Listing Price History | Yes | No | No | No |
| Real Estate (Zillow + Redfin + Realtor.com + Rightmove, 19 endpoints) | Yes | No | No | No |
| UK Sold House Prices since 1995 (Rightmove, England and Wales) | Yes | No | No | No |
| Rent.com and Apartment Guide Rentals by City, ZIP or Neighborhood, Rent per Bed Count, Deals and Price Drops, Floor Plans and Fees, City Rent Trends (US; 6 endpoints) | Yes | No | No | No |
| Trulia Neighborhood Pages with What Locals Say, Safety Statements and Market Snapshot, Homes for Sale, for Rent and Sold, Schools (US; 5 endpoints) | Yes | No | No | No |
| StreetEasy NYC and North NJ Sales, Rentals and Past Sales, Net Effective Rent, Price History, Buildings, Monthly Market Data and Indexes (5 endpoints) | Yes | No | No | No |
| RentCafe Rentals with Rent Ranges, Rent Specials, Floor Plan Units, Resident Reviews and City Rent Trends (US and Canada; 6 endpoints) | Yes | No | No | No |
| Movoto Homes for Sale, Sold and for Rent by City, ZIP, County or School Zone, Price History, Market Trends with Median Price and Days on Market (US; 5 endpoints) | Yes | No | No | No |
| HotPads Rentals by Area with Rent Ranges and Special Offers, Floor Plans, Rent History, Move-In and Monthly Costs and Fees (US; 5 endpoints) | Yes | No | No | No |
| Apartment List Rentals with Rent per Bed Count, Units Available and Rent Specials, Floor Plan Unit Prices, the City Rent Report and Market Summaries (US; 6 endpoints) | Yes | No | No | No |
| Compass Homes for Sale, for Rent and Sold, Pricing with Monthly Charges and Financing Terms, Price History and Building Details (US; 3 endpoints) | Yes | No | No | No |
| AffordableHousing.com Section 8 and Income-Restricted Rentals, Housing Waiting Lists and Housing Authorities by State (US; 6 endpoints) | Yes | No | No | No |
| Lennar New-Home Prices and Was Prices by Market, Communities, Plans, Homesites, Promotions and Monthly Payment Estimates (US; 11 endpoints) | Yes | No | No | No |
| Extra Space Storage Unit Prices by Size near a ZIP or Point, Promotions, Facility Units, Reviews and City Storage Prices (US; 5 endpoints) | Yes | No | No | No |
| Public Storage Unit Prices (Online and In-Store), Promotions and Move-In Costs, Facilities and Reviews (US and Canada; 3 endpoints) | Yes | No | No | No |
| U-Haul Truck Rental Rates for a Move, Locations, Self-Storage Facilities and Starting Rates, Reviews and Moving Supplies (US and Canada; 8 endpoints) | Yes | No | No | No |
| Travel (Booking + Airbnb + Tripadvisor, 10 endpoints) | Yes | No | No | No |
| Vrbo Vacation Rental Nightly Prices and Stay Totals for Your Dates, Deals, Ratings, Property Details and House Rules (20 market-languages; 3 endpoints) | Yes | No | No | No |
| Expedia Hotel Prices for Your Dates (Nightly, Total, Was Price), Property Details and Fees, Daily Price Calendars (51 market-languages; 4 endpoints) | Yes | No | No | No |
| Jobs & Employers (Indeed + Glassdoor, 8 endpoints) | Yes | No | No | No |
| Ad Transparency (Meta + Google, 6 endpoints) | Yes | No | No | No |
| Filings (SEC EDGAR + Companies House, 10 endpoints) | Yes | No | No | No |
| Read Any URL (`extract`) | Yes | Yes | No | Yes |
| Company Enrichment: Emails, Phones, Socials and Owner from a Website or Google Maps place_id (`company.enrich`) | Yes | No | No | No |
| Data Sources | 60 | 1 | 1 per plan | 1 |
| Structured JSON | Yes | Yes | Yes | Raw HTML |
| Knowledge Graphs | Yes | No | Yes | No |
| Async Client | Yes | Yes | No | No |
| Single API Key | Yes | Yes | No | No |
| Rate Limiting Built-in | Yes | No | No | No |
| Automatic Retries + Backoff | Yes | No | No | No |
| Fully Typed Parameters | Yes | No | No | No |
| Type Hints (PEP 561) | Yes | Yes | No | No |

Tavily focuses on AI-optimized web search. SerpAPI offers SERP parsing across search engines with separate plans. ScraperAPI provides raw web scraping with proxy rotation. Scavio combines multi-source structured data in a single [search API for AI agents](https://scavio.dev/search-api-for-ai-agents?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) with one SDK and one API key.

## Installation

```bash
pip install scavio
```

## Quick Start

Get your free API key at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient(api_key="sk_...")  # or set SCAVIO_API_KEY env var

results = client.search("best noise cancelling headphones 2026")
for r in results["organic_results"]:
    print(r["title"], r["link"])
```

Every method returns the API response as a plain `dict`. Amazon responses are
normalized to a stable, documented shape; the other endpoints keep each
platform's own field names, so fields vary by endpoint.

## Fully typed parameters

Every endpoint exposes all of its parameters as explicit, documented,
autocomplete-friendly keyword arguments with `Literal` types for enums. Your
editor shows the full parameter set, allowed enum values, and defaults inline.

```python
# Google web search with the full parameter surface
results = client.google.search(
    "electric cars",
    gl="us",                 # country of the search
    hl="en",                 # UI language
    location="Austin, Texas, United States",
    time_period="last_month",
    device="mobile",
)

# Local rank tracking: web_only=True returns Google's Web results (organic
# only, ranked for location). The standard page localizes only the local pack;
# call again without web_only when you also need local_results.
local = client.google.search("emergency plumber", location="Austin,Texas,United States", web_only=True)

# YouTube filters. The digit-named API fields (4k, 360, 3d) are exposed as
# valid Python identifiers: four_k, video_360, video_3d.
client.youtube.search("drone footage", four_k=True, hdr=True, duration="long")

# Amazon product lookup: pass the ASIN (sent to the API as `query`).
# `country` is the marketplace, as an ISO 3166-1 alpha-2 code.
client.amazon.product("B09XS7JWHH", country="gb")
```

### Forward-compatible passthrough

Any parameter the API adds in the future can be passed via `**extra` and is sent
verbatim, so you never have to wait for an SDK release:

```python
client.google.search("openai", **{"some_new_param": "value"})
```

## Retries and resilience

The client automatically retries transient failures (HTTP 429 and 5xx, plus
network/timeout errors) with exponential backoff, jitter, and `Retry-After`
support. Configure or disable it with `max_retries`.



### 1. AI Web Research -- Feed Search Results to an LLM

```python
from scavio import ScavioClient

client = ScavioClient()

results = client.search("latest advances in quantum computing 2026")

context = "\n\n".join(
    f"[{r['title']}]({r['link']})\n{r.get('snippet', '')}"
    for r in results["organic_results"]
)

prompt = f"Based on these search results, summarize the latest advances:\n\n{context}"
# Pass `prompt` to your LLM of choice (OpenAI, Anthropic, etc.)
print(prompt[:500])
```

### 2. Price Comparison -- Amazon vs Walmart

```python
from scavio import ScavioClient

client = ScavioClient()

query = "sony wh-1000xm5"
amazon = client.amazon.search(query, country="us")
walmart = client.walmart.search(query)

print("Amazon:")
for p in amazon["data"]["products"][:3]:
    print(f"  ${p['price']} - {p['title'][:60]}")

print("\nWalmart:")
for p in walmart["data"]["products"][:3]:
    print(f"  ${p['price']} - {p['title'][:60]}")
```

### 3. Product Lookup by ASIN, plus every seller offer

```python
from scavio import ScavioClient

client = ScavioClient()

data = client.amazon.product("B0BS1PRC4L")["data"]

print(f"Brand:   {data['brand']}")
print(f"Title:   {data['title']}")
print(f"Rating:  {data['rating']} ({data['reviews_count']} reviews)")
print(f"Price:   {data['price']} {data['currency']}")

# Same ASIN, every seller: price, condition, and who holds the buy box.
offers = client.amazon.offers("B0BS1PRC4L")["data"]
print(f"{offers['total_offers']} offers")
for o in offers["offers"][:5]:
    tag = " (buy box)" if o["is_buy_box_winner"] else ""
    print(f"  {o['price']} {o['currency']} - {o['seller_name']} [{o['condition']}]{tag}")
```

### 4. SEO Competitor Analysis

```python
from scavio import ScavioClient

client = ScavioClient()

results = client.search("best project management software", gl="us")

for r in results["organic_results"]:
    print(f"{r['position']}. {r['title']}")
    print(f"   {r['link']}")
```

### 4b. Migrating from the Google Custom Search JSON API -- `google.custom_search`

`google.custom_search` takes the Custom Search JSON API (`cse.list`) parameters and returns
the same `customsearch#search` response: `items[]` with `title`, `link`, `snippet` and
`displayLink`, `searchInformation.totalResults`, and `queries.nextPage`. Parsing code written
for the Custom Search JSON API keeps working. 1 credit per call.

```python
results = client.google.custom_search(
    "abortcontroller fetch timeout",
    num=5,
    site_search="stackoverflow.com",   # enforced on the returned results
    date_restrict="y1",
)
for item in results.get("items", []):
    print(item["displayLink"], item["title"], item["link"])
next_page = results["queries"].get("nextPage", [{}])[0].get("startIndex")
```

Not using this SDK? Keep your existing Custom Search code and change the host:
`https://api.scavio.dev/customsearch/v1?key=YOUR_SCAVIO_KEY&q=...`. `cx` is accepted and
ignored (use `site_search` to restrict). Parameters that cannot be honoured (image search,
`sort`, `rights`) raise `BadRequestError` instead of being silently dropped. For the full SERP
(knowledge graph, AI overview, People Also Ask) use `google.search`.
[Docs](https://scavio.dev/docs/google-custom-search-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

### 4c. AI Visibility -- What ChatGPT and Gemini Recommend -- `chatgpt.prompt` / `gemini.prompt`

Send the prompt a buyer would ask and get the answer the assistant gives: the full Markdown
answer, the pages it cites, the web searches it ran (ChatGPT) and the products it recommended.
Both return the same shape under `data`, so one parser tracks both. ChatGPT costs 2 credits and
Gemini 5 credits per answered prompt; a failed prompt is not charged. Answers take 10-40 seconds, so both methods raise the
request timeout to 120s when your client's is shorter.

```python
prompt = "What are the best CRM tools for small agencies?"

for res in (client.chatgpt.prompt(prompt, country="us"), client.gemini.prompt(prompt)):
    data = res["data"]
    answer = data["answer"]["markdown"]
    print(data["platform"], "mentions HubSpot:", "HubSpot" in answer)
    print("  cited:", [s["url"] for s in data["sources"]][:5])
    print("  products:", [p["title"] for p in data["shopping"]])

# ChatGPT also reports the web searches it ran and each source's title and publisher
data = client.chatgpt.prompt(prompt)["data"]
print(data["search_queries"])
print([(s["source"], s["title"]) for s in data["sources"]][:5])
```

[ChatGPT docs](https://scavio.dev/docs/chatgpt-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) |
[Gemini docs](https://scavio.dev/docs/gemini-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

### 5. News Aggregation

```python
from scavio import ScavioClient

client = ScavioClient()

news = client.google.news("AI startups")

for article in news["news_results"][:5]:
    print(f"[{article['source']}] {article['title']}")
    print(f"  {article['link']}")
    print()
```

### 6. YouTube Content Discovery

```python
from scavio import ScavioClient

client = ScavioClient()

videos = client.youtube.search("python tutorial", sort_by="view_count")

for v in videos["data"]["results"][:5]:
    print(f"{v['title']} ({v['view_count']:,} views)")
    print(f"  {v['url']}")

# Full details for a specific video (metadata() is a deprecated alias of video())
video = client.youtube.video("dQw4w9WgXcQ")
print(f"\n{video['data']['title']}")
print(f"  {video['data']['view_count']:,} views")

# Transcript, related videos, comments, channel, and streams
transcript = client.youtube.transcript("dQw4w9WgXcQ", format="text")
related = client.youtube.related("dQw4w9WgXcQ")
comments = client.youtube.comments("dQw4w9WgXcQ")
channel_id = client.youtube.channel_resolve("@mkbhd")["data"]["channel_id"]
channel = client.youtube.channel(channel_id)
streams = client.youtube.streams("dQw4w9WgXcQ")
```

### 7. Reddit Market Research

```python
from scavio import ScavioClient

client = ScavioClient()

posts = client.reddit.search("best mechanical keyboard")

for post in posts["data"]["results"]:
    print(f"r/{post['subreddit']} - {post['title']}")
    print(f"  {post['url']}")
    print()

# Drill into a subreddit, a single post, or a redditor. reddit.post() takes a
# url or a post_id and returns the post alone -- comments are a separate call.
feed = client.reddit.subreddit_posts("MechanicalKeyboards", sort="TOP")
detail = client.reddit.post(post_id="t3_1v6ngaf")
comments = client.reddit.post_comments("t3_1v6ngaf", sort="TOP")
history = client.reddit.user_posts("spez")
popular = client.reddit.popular()
trending = client.reddit.trending()
```

### 8. TikTok Hashtag Analysis

```python
from scavio import ScavioClient

client = ScavioClient()

hashtag = client.tiktok.hashtag(hashtag_name="python")
info = hashtag["data"]["challengeInfo"]

print(f"#{info['challenge']['title']}")
print(f"  Views: {int(info['statsV2']['viewCount']):,}")
print(f"  Videos: {int(info['statsV2']['videoCount']):,}")
```

### 9. Instagram Profile and Posts

```python
from scavio import ScavioClient

client = ScavioClient()

# Profile and reels: typically 1 credit each; most other calls 2
profile = client.instagram.profile(username="nike")
user = profile["data"]
print(f"@{user['username']} - {user['follower_count']:,} followers")

posts = client.instagram.user_posts(username="nike", count=12)
reels = client.instagram.user_reels(username="nike")
hashtags = client.instagram.search_hashtags("fashion")

# Highlights, similar accounts, likers, and Reels / audio / place search
highlights = client.instagram.user_highlights(username="natgeo")
reels_found = client.instagram.search_reels("latte art")
tracks = client.instagram.search_music("espresso")
places = client.instagram.search_locations("blue bottle coffee")
```

### 10. X Search and Profiles

```python
from scavio import ScavioClient

client = ScavioClient()

tweets = client.x.search("AI agents", search_type="Latest")
for t in tweets["data"]["timeline"][:5]:
    print(f"@{t['screen_name']}: {t['text'][:80]}")

# Profile, a user's tweets, followers, and a single tweet's replies
profile = client.x.user("elonmusk")
timeline = client.x.user_tweets("elonmusk")
followers = client.x.user_followers("elonmusk")
replies = client.x.tweet_comments("1808168603721650364", rank="top")
trending = client.x.trending(country="UnitedStates")
```

### 11. LinkedIn People and Companies

```python
from scavio import ScavioClient

client = ScavioClient()

# Member profile (1 credit) and their recent posts (10 credits per page). A
# handle or a full LinkedIn URL works anywhere.
person = client.linkedin.person(username="williamhgates")
person_posts = client.linkedin.person_posts(url="https://www.linkedin.com/in/williamhgates/")

# Company profile and its recent posts
company = client.linkedin.company(company="microsoft")
company_posts = client.linkedin.company_posts(company="microsoft")

# Jobs: search, then pull full detail for one listing
job_results = client.linkedin.search_jobs("software engineer", location="United States")
job = client.linkedin.job(job_id=job_results["data"]["data"][0]["id"])

# A post and its comments (10 per page)
post = client.linkedin.post(post_id="7488618410256523265")
comments = client.linkedin.post_comments(post_id="7488618410256523265", page=1)
```

> **Retired endpoints.** The LinkedIn data behind `person_contact`,
> `company_people`, `company_jobs`, `search_people` and `search_posts` is no
> longer available. They remain callable but always return HTTP 410 and are never
> billed. `company()` still returns `featured_employees` (a small sample of
> staff), and `search_jobs()` with a company name substitutes for `company_jobs`.

### 12. TikTok Shop Product Research

```python
from scavio import ScavioClient

client = ScavioClient()

# Listings carry exact prices
results = client.tiktok_shop.search("phone case")
for p in results["data"]["products"][:5]:
    print(p["title"], p["price"]["current"], p["shop"]["shop_name"])

# Detail adds description, variants, stock and shipping -- but NOT a price
# (TikTok masks it), and it resolves only about 44% of the ids search returns.
# A 404 there is a normal outcome, not an error: skip the item, do not retry.
from scavio import NotFoundError

product_id = results["data"]["products"][0]["product_id"]
try:
    detail = client.tiktok_shop.product(product_id)
    print(detail["data"]["title"], len(detail["data"]["variants"]), "variants")
except NotFoundError:
    pass  # TikTok Shop has no detail data for this product; skip it, do not retry

reviews = client.tiktok_shop.product_reviews(product_id, page_size=200, sort="relevant")
catalog = client.tiktok_shop.shop_products("7495514739648989419")   # exact prices
tree = client.tiktok_shop.categories()
resolved = client.tiktok_shop.resolve("https://vt.tiktok.com/ZT2AHoGsE/")
```

### 13. Social Media Monitoring

```python
from scavio import ScavioClient

client = ScavioClient()

brand = "scavio"
reddit = client.reddit.search(brand)
tiktok = client.tiktok.search_videos(brand, count=5)

print(f"Reddit mentions ({len(reddit['data']['results'])}):")
for post in reddit["data"]["results"][:3]:
    print(f"  r/{post['subreddit']}: {post['title']}")

tiktok_videos = tiktok["data"].get("search_item_list", [])
print(f"\nTikTok mentions ({len(tiktok_videos)}):")
for v in tiktok_videos[:3]:
    desc = v["aweme_info"].get("desc", "No description")
    print(f"  {desc[:80]}")
```

### 14. Price Drop Alert

```python
from scavio import ScavioClient

client = ScavioClient()

product = client.walmart.product("123456789")
price = product["data"]["price"]
title = product["data"]["title"]

threshold = 50.00
if price and price < threshold:
    print(f"PRICE DROP: {title[:60]}")
    print(f"  Now ${price} (threshold: ${threshold})")
else:
    print(f"{title[:60]}: ${price}")
```

### 15. Async Multi-Source Search

```python
import asyncio
from scavio import AsyncScavioClient

async def main():
    async with AsyncScavioClient() as client:
        google = await client.search("mechanical keyboard")
        amazon = await client.amazon.search("mechanical keyboard", country="us")

        print(f"Google: {len(google['organic_results'])} results")
        print(f"Amazon: {len(amazon['data']['products'])} products")

        for r in google["organic_results"][:3]:
            print(f"  Web: {r['title'][:60]}")
        for p in amazon["data"]["products"][:3]:
            print(f"  Amazon: ${p['price']} - {p['title'][:50]}")

asyncio.run(main())
```

### 16. Check API Usage

```python
from scavio import ScavioClient

client = ScavioClient()

usage = client.get_usage()
print(f"Plan: {usage['plan']}")
print(f"Credits remaining: {usage['credit_balance']}")
```

### 17. Read Any URL -- `extract()`

`extract` is a core capability, not a platform. `client.extract(url)` reads one
page; the same `client.extract` object also maps, crawls and batch-extracts
whole sites (example 17b). It is the "read this page" primitive an agent
reaches for when the page is not on a site Scavio has a dedicated namespace for.

```python
from scavio import ScavioClient

client = ScavioClient()

# Default: readability Markdown, normal mode. 1 credit.
page = client.extract("https://example.com/blog/post")["data"]
print(page["content_length"], "chars of", page["format"])
print(page["content"][:500])

# format="html" is the raw page; format="text" is the Markdown flattened.
raw = client.extract("https://example.com/blog/post", format="html")

# mode is the price-bearing parameter, and the only knob that matters on a
# hard target: "normal" (1 credit) -> "advanced" for JavaScript-built pages
# (1 credit) -> "ultra" for the hardest pages (2 credits).
hard = client.extract("https://example.com/spa", format="markdown", mode="ultra")

# Billing is charged only on a successful extraction: a dead link, a bot wall
# or a timeout costs nothing, so retrying up a tier is safe.
```

### 17b. Map, Crawl and Batch-Extract Whole Sites -- `extract.map / crawl / batch`

Three multi-page operations hang off `client.extract`:

| Call | What it returns | Price |
|---|---|---|
| `extract.map(url, ...)` | A site's page URLs from its sitemaps and start page, deduplicated and path-filtered (synchronous) | 1 credit on the normal tier (up to 2 on `advanced`, up to 10 on `ultra`) |
| `extract.crawl(url, ...)` | A job that discovers and extracts same-site pages breadth-first, each as Markdown, text or HTML | Per **successful** page at extract's price: 1 (`normal`, `advanced`) or 2 (`ultra`) |
| `extract.batch(urls, ...)` | A job that extracts a list of URLs, results in input order | Same per-page price; invalid URLs are reported and never billed |
| `extract.crawl_status(job_id)` / `extract.batch_status(job_id)` | Progress (`status`, `pages`, `credits_used`, `stopped_reason`) and one page of results with `next_cursor` | Free |
| `extract.cancel_crawl(job_id)` / `extract.cancel_batch(job_id)` | Stops a queued or running job; results so far stay available (409 if it already finished) | Free |

Failed and skipped pages cost nothing, starting a job costs nothing, and credits
are taken page by page: if your balance runs out the job stops cleanly with
`stopped_reason="insufficient_credits"`. robots.txt is always obeyed for map
and crawl. A crawl stays on the start URL's site (subdomains optional via
`allow_subdomains=True`) and visits URLs under the start path first. Results
are kept for 3 days after a job finishes (up to 2 MB per page, 250 MB per job);
a job runs for at most 6 hours.

| Plan | Max pages per crawl | Active jobs | URLs per batch |
|---|---|---|---|
| Free | 10 | 1 | 10 |
| PAYG | 100 | 1 | 50 |
| Project | 500 | 2 | 100 |
| Bootstrap | 2,000 | 3 | 500 |
| Startup | 5,000 | 5 | 1,000 |
| Growth | 10,000 | 10 | 1,000 |

Starting a job beyond your active-job limit raises `RateLimitError` (429).

```python
from scavio import ScavioClient

client = ScavioClient()

# Map: every URL on a site, filtered. Synchronous, 1 credit.
site = client.extract.map("https://scavio.dev", include_paths=["/docs/**"], limit=200)
for link in site["data"]["links"]:
    print(link["url"], link["source"], link.get("lastmod"))

# Crawl and wait: polls until the job finishes, then pages through every
# result for you. Two pages here, so 2 credits on the normal tier.
crawl = client.extract.crawl("https://scavio.dev/docs", max_pages=2, wait=True)
for page in crawl["data"]["results"]:
    print(page["url"], page["status"], page["content_length"])

# Or start it and poll yourself (better for large crawls).
job = client.extract.crawl(
    "https://example.com/blog",
    max_pages=500,
    max_depth=2,
    exclude_paths=["/blog/tag/**"],
    format="markdown",
)["data"]
status = client.extract.crawl_status(job["id"], include_content=False)
print(status["data"]["status"], status["data"]["pages"])

# Page through results with next_cursor (1-100 per call, default 25).
cursor = None
while True:
    page = client.extract.crawl_status(job["id"], cursor=cursor, limit=100)["data"]
    for result in page["results"]:
        ...  # result["url"], result["status"], result["content"]
    cursor = page["next_cursor"]
    if not cursor:
        break

# Batch: a list of URLs in one job, results in input order.
batch = client.extract.batch(
    ["https://example.com/a", "https://example.com/b"], format="text", wait=True
)
print(batch["data"]["pages"])
```

`wait=True` is a convenience: it polls every `poll_interval` seconds (default
2) and returns `{"data": {...final status..., "results": [...every page...],
"next_cursor": None}, "created": {...the job as created...}}`. Pass
`wait_timeout=` (seconds) to bound it; on expiry it raises
`ScavioJobTimeoutError`, whose `job_id` you can keep polling, while the job
keeps running on the server. Without `wait` you get the queued job back at once
(`id`, `status`, `status_url`, `credits_per_page`, and for batch `urls_count`
and `invalid_urls`).

Every crawl and batch POST carries an `Idempotency-Key` header. Pass your own
with `idempotency_key=` to make a retried request return the original job
within 24 hours; when you pass none, the SDK generates one per call so its own
automatic retries never start a second job. The async client has the same
surface: `await client.extract.crawl(...)`.

#### Completion webhooks

Pass `webhook_url="https://..."` to `crawl` or `batch` and Scavio POSTs the
final job status there when it completes, fails or is cancelled (retried after
30 seconds and 5 minutes on failure). The job creation response carries a
`webhook_secret`, returned only once; store it. Each delivery is signed with
`Scavio-Signature: t=<unix>,v1=<hex>`, an HMAC-SHA256 of `"<t>.<raw body>"`.
Verify it with `scavio.verify_webhook`, passing the RAW request body:

```python
import scavio

job = client.extract.crawl(
    "https://example.com/docs", webhook_url="https://hooks.example.com/scavio"
)["data"]
secret = job["webhook_secret"]  # store it: it is returned only once

# In your webhook handler (Flask shown):
from flask import Flask, abort, request

app = Flask(__name__)

@app.post("/scavio")
def scavio_webhook():
    if not scavio.verify_webhook(
        secret, request.headers.get("Scavio-Signature"), request.get_data()
    ):
        abort(401)
    event = request.get_json()
    print(event["id"], event["status"])
    return "", 204
```

`verify_webhook(secret, header, body, tolerance=300)` returns `False` for a
missing, malformed, tampered or stale (older than `tolerance` seconds)
signature, and compares in constant time.

### 18. eBay Price Research -- Sold Listings, Not Asking Prices

Live listings tell you what sellers *want*. `sold=True` searches completed
listings that actually sold, which is what a pricing model needs.

```python
from scavio import ScavioClient

client = ScavioClient()

sold = client.ebay.search(
    query="airpods pro 2",
    sold=True,
    condition="used",
    per_page=240,          # 60, 120 or 240 only; anything else falls back to 60
    min_price=50,          # prices are numbers, so 49.99 is legal too
)["data"]

prices = sorted(p["price"] for p in sold["products"] if p.get("price"))
print("median sold price:", prices[len(prices) // 2])

# On the sold view eBay publishes no headline count, so total_results is null.
# Page with `page` until a page comes back empty rather than trusting a total.
assert sold["total_results"] is None

# On the LIVE view total_results is eBay's own estimate and an unstable one --
# four identical requests minutes apart reported 28k, 140k, 170k and 27k.
# Treat it as an order of magnitude, never as a count.

# `seller` works with no query at all, which is how you page a whole catalogue.
# ebay.seller() is a profile card only -- it cannot enumerate inventory.
catalogue = client.ebay.search(seller="mytechstore", page=1)["data"]
profile = client.ebay.seller("mytechstore")["data"]
```

### 19. Meta Ad Library -- Walking a Competitor's Whole Ad Set

Meta pages the ad library by cursor, and the first page is a different size
from the rest: 30 ads on page 1, then 10 per cursor page.

```python
from scavio import ScavioClient

client = ScavioClient()

ads, cursor = [], None
while True:
    # page_id is the advertiser's numeric Facebook Page id, as a string.
    page = client.meta_ads.advertiser("20531316728", cursor=cursor)["data"]
    ads.extend(page["ads"])
    if not page["has_next_page"]:
        break
    cursor = page["next_cursor"]

print(len(ads), "ads")

# Every page is 1 credit, and past the first 30 ads a page is 10 ads, so a deep
# walk costs roughly one credit per ten ads. Budget for depth.

# Keyword search pages the same way. total_results caps at 50000 with
# total_is_capped true, because Meta itself only reports ">50,000" -- never
# present it as an exact count.
first = client.meta_ads.search(
    "black friday", country="US", active_status="active"
)["data"]
if first["total_is_capped"]:
    print("more than", first["total_results"], "ads match")

# Spend, reach, impressions and the paid-for-by disclosure are political-only.
# On commercial ads they are null by design, not a bug.
political = client.meta_ads.search("vote", ad_type="political_and_issue_ads")["data"]

# The cursor is a self-contained blob: every other filter is ignored while it
# is set, so do not "change the filter and keep paging" -- start a new walk.
```

### 20. Costco -- Warehouse Prices, Stock, Gas, Coupons and Clearance

`costco` covers costco.com and costco.ca (`country="ca"`); `search`, `product`
and `warehouses` also take the international sites (uk, au, mx, jp, kr, tw).
Warehouse numbers come from `warehouses()`; pass one as `warehouse_id` to add
that warehouse's in-store price, stock status and price code to every search,
category or deals result.

```python
from scavio import ScavioClient

client = ScavioClient()

# Nearest warehouses to a US zip code, with hours, services and gas prices.
near = client.costco.warehouses(zip="10025", limit=3)["data"]

# Search with one warehouse's in-store price alongside the online price.
oil = client.costco.search("olive oil", warehouse_id="1062", page_size=5)["data"]
for item in oil["results"]:
    print(item["title"], item["price"], item["warehouse"]["price"])

# Online vs in-warehouse price at up to 10 warehouses, with discount, final
# price and promotion dates. 1 credit for up to 9 warehouses, 2 for 10.
prices = client.costco.prices(item_id="1492456", warehouse_ids=["1062", "1107"])["data"]
for row in prices["items"][0]["warehouses"]:
    print(row["warehouse_id"], row["price"], row["final_price"])

# In-warehouse stock status (a status, never a quantity). 1 credit per 5 warehouses.
stock = client.costco.availability("1492456", ["1062"])["data"]

# Regular, premium and diesel prices near a location, or at given warehouses.
gas = client.costco.gas(zip="90001")["data"]
for station in gas["stations"]:
    print(station["name"], station["prices"]["regular"], station["prices"]["premium"])

# The current member coupon book (US), and the deal feeds.
book = client.costco.coupons()["data"]
hunt = client.costco.deals("treasure_hunt")["data"]

# Markdown finder at one warehouse: .97 clearance and .00/.88 manager markdowns
# by default; add special_buy for .49/.79/.89 endings. The codes are the
# member-community decode -- Costco does not publish them.
marked_down = client.costco.clearance("1062", query="snacks")["data"]
print(marked_down["count"], "of", marked_down["products_scanned"], "items marked down")
```

### 21. Trustpilot -- Business Search, Profiles, Reviews and Categories

`trustpilot` finds businesses by keyword or category, reads a full profile
(TrustScore, rating distribution, reply rate and days to reply on negative
reviews, AI summary and topics when Trustpilot has them), and pages filtered
reviews. Every call costs 2 credits. `business()` and `reviews()` take exactly
one of `domain` or `url`.

```python
from scavio import ScavioClient

client = ScavioClient()

# Businesses matching a keyword, up to 100 per page. Email and phone appear
# only when the business published them.
found = client.trustpilot.search("vpn", country="US", page_size=10)["data"]
for biz in found["businesses"]:
    print(biz["name"], biz["domain"], biz["trust_score"], biz["review_count"], biz["email"])

# One profile with the rating distribution, reply behavior and 20 newest reviews.
profile = client.trustpilot.business(domain="nordvpn.com")["data"]
print(profile["trust_score"], profile["rating_distribution"])
print(profile["reply_behavior"]["reply_rate"], profile["reply_behavior"]["avg_days_to_reply"])
topic_ids = [t["id"] for t in profile["topics"]]  # feed these to reviews(topics=...)

# Filtered reviews, 20 per page. Trustpilot serves up to 10 pages (200 reviews)
# per filter combination; max_page says how far this one goes. Slice by stars,
# language, date_range, topics or search to reach more. total_filtered counts
# every match, so a date range doubles as review velocity.
bad = client.trustpilot.reviews(
    domain="nordvpn.com", stars=[1, 2], language="en", date_range="last30days"
)["data"]
print(bad["total_filtered"], "1-2 star reviews in 30 days; pages:", bad["max_page"])
for review in bad["reviews"]:
    print(review["rating"], review["title"], (review["reply"] or {}).get("text"))

# The category tree, then ranked businesses in one category. min_trust_score is
# a star-rating floor: Trustpilot rounds TrustScore to stars, so 4 includes 3.8+.
tree = client.trustpilot.categories()["data"]
print(tree["count"], "top-level,", tree["subcategory_count"], "subcategories")
ranked = client.trustpilot.category(
    "vpn_service", sort="reviews_count", min_trust_score=4, claimed_only=True
)["data"]
for biz in ranked["businesses"]:
    print(biz["name"], biz["trust_score"], biz["website"])

# One review by id, with the business it is about.
one = client.trustpilot.review("6aca2504b52cc4b518bf4b75")["data"]
print(one["review"]["text"], one["business"]["name"])
```

An unknown business, review or category returns a 404 (`NotFoundError`) and is
billed 2 credits. Trustpilot keeps no TrustScore history, so none is returned.

### 22. Realtor.com and Rightmove -- Listings, Sold Comps and Agents

`realtor` covers US listings (for sale, pending, for rent and sold) with up to
200 rows per call, full property detail, market stats and agents. `rightmove`
covers UK listings, England and Wales sold house prices since 1995 and agent
branches. Every call on both costs 1 credit.

Docs: Realtor.com [search](https://scavio.dev/docs/realtor-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [property](https://scavio.dev/docs/realtor-property?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [locations](https://scavio.dev/docs/realtor-locations?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [market](https://scavio.dev/docs/realtor-market?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [agents](https://scavio.dev/docs/realtor-agents?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [agent](https://scavio.dev/docs/realtor-agent?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme); overview at the [Realtor.com API](https://scavio.dev/realtor-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) page.
Rightmove [search](https://scavio.dev/docs/rightmove-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [property](https://scavio.dev/docs/rightmove-property?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [sold](https://scavio.dev/docs/rightmove-sold?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [sold property](https://scavio.dev/docs/rightmove-sold-property?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [locations](https://scavio.dev/docs/rightmove-locations?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [agents](https://scavio.dev/docs/rightmove-agents?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [agent](https://scavio.dev/docs/rightmove-agent?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme); overview at the [Rightmove API](https://scavio.dev/rightmove-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) page.

```python
from scavio import ScavioClient

client = ScavioClient()

# Sold land comps: 200 rows per call, filtered by lot size, price and recency.
# Realtor.com serves the first 10,000 results of a search; slice by price band,
# property type or area to go further. Sold prices are null in US non-disclosure
# states (Texas, Utah, Wyoming and others); sold dates still come back.
comps = client.realtor.search(
    location="Maricopa County, AZ",
    listing_status="sold",
    property_types=["land"],
    sold_within_days=365,
    lot_sqft_min=43560,
    page_size=200,
)["data"]
print(comps["total"], "sold; pages:", comps["max_page"])
for row in comps["listings"]:
    print(row["sold_price"], row["sold_date"], row["lot_sqft"], row["address"]["line"])

# Listing-text keyword watch, then one property in full. A listing must contain
# ALL the keywords you pass, so each extra keyword narrows the results.
shops = client.realtor.search(location="Austin, TX", keywords=["workshop"])["data"]
detail = client.realtor.property(property_id=shops["listings"][0]["property_id"])["data"]
print(detail["list_price"], detail["risk"]["flood_factor"], len(detail["property_history"]))

# Autocomplete -> market stats, and agents by ZIP code.
slug = client.realtor.locations("Austin")["data"]["locations"][0]["slug_id"]
market = client.realtor.market(slug)["data"]
print(market["median_listing_price"], market["median_days_on_market"])
agents = client.realtor.agents(postal_code="78744")["data"]
profile = client.realtor.agent(agents["agents"][0]["agent_id"])["data"]
print(profile["name"], profile["rating"], len(profile["reviews"]))

# Rightmove: resolve a place, search for sale (24-25 per page, up to 42 pages).
# There is no keyword filter; match on summary and key_features yourself.
loc = client.rightmove.locations("Bristol")["data"]["locations"][0]["location_id"]
homes = client.rightmove.search(location_id=loc, property_types=["terraced"], max_price=350000)
for home in homes["data"]["listings"]:
    print(home["price_display"], home["address"], home["tenure"])

# Sold prices since 1995 for an outcode (England and Wales only), then one
# address's full history.
sold = client.rightmove.sold("BS3", sold_within_years=5)["data"]
print(sold["summary"]["average_price_last_year"])
history = client.rightmove.sold_property(sold_id=sold["properties"][0]["sold_id"])["data"]
for sale in history["transactions"]:
    print(sale["date"], sale["price_display"], sale["tenure"], sale["percent_change"])

# Agent branches in an area, then one branch.
branches = client.rightmove.agents(location="Bristol")["data"]
branch = client.rightmove.agent(branch_id=branches["agents"][0]["branch_id"])["data"]
print(branch["name"], branch["listings"]["for_sale_count"], branch["listings"]["to_rent_count"])
```

An unknown property, listing, sold id, agent or branch returns a 404
(`NotFoundError`) and is billed 1 credit; a removed Rightmove listing is also a
404. Rightmove serves 42 search pages, 40 sold pages and 50 agent pages per
query.

### 23. Mercado Libre -- Listings, Products, Reviews, Questions and Best Sellers

`mercadolibre` covers Mercado Libre in Mexico, Argentina and Colombia and
Mercado Livre in Brazil (`country="mx"`, `"br"`, `"ar"` or `"co"`; prices come
back in MXN, BRL, ARS or COP). `reviews` costs 1 credit; `search`, `product`,
`questions` and `best_sellers` cost 2. Chile is not supported.

Docs: Mercado Libre [search](https://scavio.dev/docs/mercadolibre-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [product](https://scavio.dev/docs/mercadolibre-product?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [reviews](https://scavio.dev/docs/mercadolibre-reviews?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [questions](https://scavio.dev/docs/mercadolibre-questions?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [best sellers](https://scavio.dev/docs/mercadolibre-best-sellers?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme); overview at the [Mercado Libre API](https://scavio.dev/mercadolibre-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) page.

```python
from scavio import ScavioClient

client = ScavioClient()

# Search by keyword (about 48 rows per page, up to 42 pages, so about 2,000
# results per query; slice by price range, condition or seller to reach more).
found = client.mercadolibre.search(
    "iphone 15",
    country="mx",
    free_shipping=True,
    sort="price_asc",
)["data"]
print(found["total"], found["auto_applied_filters"])
for row in found["results"]:
    # sold_quantity_min is a lower bound ("+1000 vendidos"), never an exact count.
    # review_count is null when the page shows none (most sponsored rows).
    print(row["price"], row["brand"], row["rating"], row["review_count"], row["sold_quantity_min"], row["title"])

# One catalog product: price, buy-box seller with reputation, star distribution.
product = client.mercadolibre.product(product_id="MLM1027172667")["data"]
print(product["price"], product["seller"]["nickname"], product["rating"]["distribution"])

# A seller's catalogue: the buy-box seller_id feeds a filtered search.
catalogue = client.mercadolibre.search(
    country="mx", seller_id=str(product["seller"]["seller_id"]), condition="new"
)["data"]

# Reviews (15 per page, 1 credit), e.g. only 1-star; original_text keeps the
# untranslated review and country says where it was written.
reviews = client.mercadolibre.reviews(product_id="MLM1027172667", rating=1)["data"]
for review in reviews["reviews"]:
    print(review["rating"], review["country"], review["text"])

# Buyer questions with the seller's answers; page with next_offset.
qa = client.mercadolibre.questions(product["item_id"])["data"]
for q in qa["questions"]:
    print(q["text"], "->", q["answer"]["text"] if q["answer"] else None)

# Top 20 best sellers in a category (mx, ar or co; not Brazil). The category
# prefix must match the country.
top = client.mercadolibre.best_sellers(product["category_id"], country="mx")["data"]
for row in top["results"]:
    print(row["rank"], row["price"], row["sold_label"], row["title"])
```

A zero-result search returns an empty page and is billed. An unknown product,
item or seller nickname returns a 404 (`NotFoundError`) and is billed, as does a
listing with no public questions. Only the buy-box seller is returned per
product, and Brazil and Argentina may auto-apply a "new" condition (listed in
`auto_applied_filters`).

### 24. Store-Level Retail -- Lowe's, Sam's Club, Canadian Tire and Dollar General

Four retailers whose prices and stock are per store. Each answers for ONE
store you choose: find its number with the locator (`lowes.stores`,
`sams_club.clubs`, `canadian_tire.stores`, `dollar_general.stores`) and pass it
on every call. Lowe's `search`, `product` and `stores` cost 2 credits and
`reviews` 1; Sam's Club `clubs` costs 1 and its other methods 2; every Canadian Tire and Dollar General method costs 1.

```python
from scavio import ScavioClient

client = ScavioClient()

# --- Lowe's: store_id AND that store's own ZIP are required on search/product.
store = client.lowes.stores("28117", limit=1)["data"]["stores"][0]
sid, zip_code = store["store_id"], store["address"]["postal_code"]

drills = client.lowes.search(sid, zip_code, query="cordless drill")["data"]
for p in drills["products"]:
    print(p["item_id"], p["price"], p["original_price"], p["stock_quantity"], p["title"])

# Deals are search(on_sale=True); there is no clearance endpoint.
deals = client.lowes.search(sid, zip_code, query="cordless drill", on_sale=True)["data"]

item = client.lowes.product("5016412045", sid, zip_code)["data"]
print(item["price"], item["stock_quantity"], item["aisle_locations"])
for near in item["pickup"]["nearby_stores"]:
    print(near["store_id"], near["distance_miles"], near["quantity"])

reviews = client.lowes.reviews("5016412045", sort="most_helpful")["data"]  # 1 credit
for r in reviews["reviews"]:
    print(r["rating"], r["verified_purchase"], r["title"])

# --- Sam's Club: search, savings and category answer for a club picked by
# location (echoed in data.club). For one specific club, use product(club_id=).
club = client.sams_club.clubs("75201", limit=1)["data"]["clubs"][0]
found = client.sams_club.search("paper towels", sort="price_low")["data"]
for p in found["products"]:
    print(p["item_id"], p["price"], p["was_price"], p["availability_status"], p["title"])

product = client.sams_club.product("15325822107", club_id=club["club_id"])["data"]
print(product["club_price"]["price"], product["in_stock_at_club"], product["aisle"])
for option in product["fulfillment"]["options"]:
    # available_quantity is capped at 8 by the site: 8 means 8 or more.
    print(option["method"], option["availability_status"], option["available_quantity"])

savings = client.sams_club.savings(sort="top_selling")["data"]        # Instant Savings
clearance = client.sams_club.category("1150109")["data"]              # clearance
reviews = client.sams_club.reviews("15325822107", sort="lowest")["data"]

# --- Canadian Tire: prices are in CAD and differ by store and province.
stores = client.canadian_tire.stores(postal_code="M5V 2T6", sku="0438858")["data"]
for s in stores["stores"]:
    print(s["store_id"], s["name"], s["distance_km"], s["quantity"], s["aisle"])

found = client.canadian_tire.search("600", query="dewalt drill")["data"]
for p in found["products"]:
    print(p["code"], p["sku"], p["price"], p["was_price"], p["store_quantity"], p["title"])

detail = client.canadian_tire.product("0547273P", "600")["data"]
stock = client.canadian_tire.availability("600", ["0438858", "0547273"])["data"]  # up to 50 SKUs
for i in stock["items"]:
    print(i["sku"], i["price"], i["is_clearance"], i["quantity"], i["aisle"])
print("unknown:", stock["not_found"])

clearance = client.canadian_tire.clearance("600")["data"]             # in-stock only by default
sale = client.canadian_tire.deals("600", "sale")["data"]              # or instant_rebate, special_buy, loyalty

# --- Dollar General: one call gives a product's unit count at up to 25 stores.
nearby = client.dollar_general.stores(zip="75203", upc="030772156629")["data"]
for s in nearby["stores"]:
    print(s["store_id"], s["address"], s["city"], s["distance_miles"], s["quantity"], s["in_stock"])

found = client.dollar_general.search("paper towels", "12629", in_stock_only=True)["data"]
for p in found["products"]:
    print(p["upc"], p["price"], p["original_price"], p["available_quantity"], p["title"])

item = client.dollar_general.product("030772156629", "12629")["data"]
print(item["price"], item["available_quantity"], item["nearby_stores_with_stock"])

# Clearance items carry the current price only (no was-price).
on_sale = client.dollar_general.deals("12629", "on_sale")["data"]
clearance = client.dollar_general.deals("12629", "clearance")["data"]
for c in client.dollar_general.coupons()["data"]["coupons"]:
    print(c["summary"], c["brand"], c["expiration_date"])
```

Canadian Tire and Dollar General return a rating and review count but no review
text. Sam's Club's search, savings and category results reflect the club in
`data.club`, not a club you pick.

### 25. US Retail -- Sephora, Ulta Beauty, ALDI, Micro Center, Walgreens and CVS

Six US retailers (Sephora also reads Sephora Canada with `country="ca"`, see
[section 82](#82-sephora-canada----cad-prices-sale-prices-dated-offers-stores)). Sephora and Ulta Beauty carry per-shade prices and stock;
ALDI prices are per store and per shopping mode; Micro Center stock is per
store; Walgreens and CVS prices are national while stock is per store. Every
method costs 1 credit except Micro Center `search` and `product` (2), Walgreens
`search`, `product` and `stores` (2) and Walgreens `stock` (4).

```python
from scavio import ScavioClient

client = ScavioClient()

# --- Sephora: search, then one product with every shade and the review summary.
found = client.sephora.search("lipstick", sort="best_selling", zip="10001")["data"]
for p in found["products"]:
    print(p["product_id"], p["brand"], p["price"], p["rating"], p["same_day_eligible"], p["name"])

lips = client.sephora.category("lipstick")["data"]                  # same product shape
item = client.sephora.product(url=found["products"][0]["url"])["data"]  # url is faster than product_id
print(item["review_summary"])                                       # no review text
for s in item["review_sentiments"]:
    print(s["type"], s["sentiment"], s["count"])                    # pros / cons with counts
for sku in item["skus"]:
    print(sku["sku_id"], sku["variation_value"], sku["price"], sku["in_stock"], sku["only_few_left"])

# --- Ulta Beauty: stores() is in stock / out of stock at the 10 stores nearest a ZIP.
found = client.ulta.search("lipstick")["data"]
p = found["products"][0]
print(p["product_id"], p["sku_id"], p["list_price"], p["sale_price"], p["variant_label"])

detail = client.ulta.product(p["url"])["data"]
print(detail["availability"], detail["gtin"], [v["sku_id"] for v in detail["variants"]])
stores = client.ulta.stores(p["product_id"], p["sku_id"], "10001")["data"]
for s in stores["stores"]:
    print(s["store_id"], s["name"], s["distance_miles"], s["in_stock"], s["availability"])

# --- ALDI: prices are one store's and one shopping mode's. service_type is
# instore (default, the shelf price), pickup or delivery (often higher).
store = client.aldi.stores("33131", limit=1)["data"]["stores"][0]
milk = client.aldi.search("milk", store_id=store["store_id"])["data"]
for p in milk["products"]:
    print(p["product_id"], p["price"], p["was_price"], p["unit_price"], p["in_store_location"], p["name"])

online = client.aldi.search("milk", zip="33131", service_type="delivery")["data"]  # nearest store
item = client.aldi.product("16902710", store_id=store["store_id"])["data"]
print(item["price"], item["in_stock"], item["ingredients"], item["warnings"])

# --- Micro Center: stock is per 3-digit store_id; omit it for the web store
# (029, shippable items only). Counts are capped at 25+ (quantity_capped).
dallas = [s for s in client.micro_center.stores(state="TX")["data"]["stores"] if s["name"] == "Dallas"][0]
gpus = client.micro_center.search(query="rtx 5070", store_id=dallas["store_id"])["data"]   # 2 credits
for p in gpus["products"]:
    print(p["product_id"], p["price"], p["stock"]["label"], p["stock"]["quantity"], p["open_box"])

gpu = client.micro_center.product("691231", store_id=dallas["store_id"])["data"]          # 2 credits
print(gpu["selected_store"]["stock"], gpu["selected_store"]["open_box"])
print([s["store_id"] for s in gpu["stores_in_stock"] if s["in_stock"]])                  # yes/no per store

# --- Walgreens: prices are national; stock() checks up to 20 stores in one call.
nearby = client.walgreens.stores(zip="60614", limit=5)["data"]                # 2 credits
numbers = [s["store_number"] for s in nearby["stores"]]
found = client.walgreens.search("shampoo", sort="top_sellers", store_id=numbers[0])["data"]
p = found["products"][0]
print(p["product_id"], p["price"], p["sale_price"], p["availability"]["text"])

stock = client.walgreens.stock(p["product_id"], numbers)["data"]              # 4 credits
for s in stock["stores"]:
    print(s["store_number"], s["status"], s["quantity"], s["in_stock"])
print("unknown:", stock["unknown_store_ids"])

# --- CVS: there is no store locator; the store number is on every cvs.com
# store page ("Store ID: #7019"). search defaults to store 7019 (New York).
found = client.cvs.search("toothpaste", store_id="7019")["data"]
for p in found["products"]:
    print(p["sku_id"], p["price"], p["sale_price"], p["stock"]["in_store"], p["stock"]["pickup"])

# product() can take 10-30+ seconds; the SDK raises its timeout to 120s for it.
item = client.cvs.product(product_id="832677")["data"]
print(item["upc"], item["promo"], item["promo_end_date"], [v["sku_id"] for v in item["variants"]])

units = client.cvs.stock(["832677", "789787"], "7019")["data"]                 # up to 20 SKUs
for i in units["items"]:
    print(i["sku_id"], i["in_store"], i["pickup"], i["ship"])
```

Walgreens and CVS cover retail (front-store) products, not the pharmacy. An
unknown CVS SKU or store number reads as 0 units rather than an error.

### 26. US Retail -- Whole Foods Market, Harbor Freight, PetSmart, Petco, iHerb, Chewy and Menards

Seven more US retailers. Whole Foods prices are per store; Harbor Freight,
PetSmart, Petco, iHerb and Chewy prices are national; Menards prices carry the
mail-in rebate. Every method costs 1 credit except iHerb (2 each), Chewy (10
each) and Menards `product` with a `store_id` (2).

```python
from scavio import ScavioClient

client = ScavioClient()

# --- Whole Foods Market: prices are one store's (5-digit store_id, default 10145,
# Lamar in Austin TX): regular, sale and Prime member price. No per-store stock.
store = client.whole_foods.stores("10019")["data"]["stores"][0]
milk = client.whole_foods.search("milk", store_id=store["store_id"], sort="price_asc")["data"]
for p in milk["products"]:
    print(p["asin"], p["regular_price"], p["sale_price"], p["prime_price"], p["price_unit"], p["name"])

deals = client.whole_foods.deals(store_id=store["store_id"], category="cheese")["data"]
item = client.whole_foods.product(asin="B078WVT2BC", store_id=store["store_id"])["data"]
print(item["in_store"]["regular_price"], item["online"]["price"], item["online"]["availability"])

flyer = client.whole_foods.sales_flyer(store["store_id"])["data"]
for promo in flyer["promotions"]:
    print(promo["headline"], promo["sale_price"], promo["prime_price"], promo["end_date"], promo["asins"])

# --- Harbor Freight: national prices with sale, public coupon, Inside Track Club
# member price and the competitor price it quotes (compare_at).
prices = client.harbor_freight.prices(["73216", "59716"])["data"]
for p in prices["products"]:
    print(p["sku"], p["price"], p["regular_price"], p["sale"], p["coupon"], p["member_deal"], p["compare_at"])

found = client.harbor_freight.search(query="cordless drill")["data"]
print(found["redirect"])                       # set when a keyword maps to a category page
drills = client.harbor_freight.search(category_id="1827", sort="price_low")["data"]

# Stock is a status (in_stock, limited, out_of_stock, not_carried) plus the
# aisle, from a daily snapshot -- not a unit count.
stock = client.harbor_freight.availability(["73216"], zip="90012", limit=5)["data"]
print(stock["inventory_updated_at"])
for s in stock["stores"]:
    for i in s["items"]:
        print(s["store_id"], s["name"], i["sku"], i["stock_status"], i["aisle"])

# --- PetSmart: national prices with the Autoship first-order and recurring
# price; stock is a unit count per store.
found = client.petsmart.search("dog food", store_id="1658")["data"]   # in stock at that store
p = found["products"][0]
item = client.petsmart.product(web_style_id=p["web_style_id"])["data"]
for v in item["variants"]:
    print(v["sku"], v["options"], v["price"], v["sale_price"], v["autoship"])  # autoship: first_order_price, recurring_price

stock = client.petsmart.store_stock("1658", [v["sku"] for v in item["variants"]])["data"]
for i in stock["items"]:
    print(i["sku"], i["store_quantity"], i["ship_to_home_quantity"])
pairs = client.petsmart.availability([{"store_id": "1658", "sku": "5252900"}, {"store_id": "2528", "sku": "5252900"}])
sale = client.petsmart.deals(pet="dog")["data"]
print([p["name"] for p in sale["products"] if p["on_sale"]])   # the Sale section also lists non-price promotions

# --- Petco: national price plus the Repeat Delivery (autoship) price. Store
# inventory takes cat_entry_id (from search or product), not the part number.
found = client.petco.search("dog food")["data"]
p = found["products"][0]
print(p["part_number"], p["cat_entry_id"], p["price"], p["list_price"], p["autoship_price"])

# Petco calls can take 10-30 seconds; the SDK raises their timeout to 120s.
item = client.petco.product(url=p["url"])["data"]
for v in item["variants"]:
    print(v["cat_entry_id"], v["price"], v["autoship_price"], v["first_autoship_price"], v["online_quantity"])

store = client.petco.stores("10001", limit=1)["data"]["stores"][0]
inv = client.petco.store_inventory([v["cat_entry_id"] for v in item["variants"]], store_id=store["store_id"])["data"]
for i in inv["items"]:
    print(i["cat_entry_id"], i["qty_available"], i["alert_level"], i["in_stock"])

# --- iHerb: online only (no stores), US store in USD. 2 credits per call.
# search() and product() can take 10-25 seconds; the SDK raises their timeout to 120s.
found = client.iherb.search("vitamin d", sort="best_selling")["data"]
ids = [p["product_id"] for p in found["products"][:10]]
for row in client.iherb.prices(ids)["data"]["products"]:          # up to 50 ids
    print(row["product_id"], row["found"], row["price"], row["list_price"], row["in_stock"])

summary = client.iherb.reviews(product_id=ids[0])["data"]        # summary, not a review list
print(summary["average_rating"], summary["rating_histogram"]["five"], summary["top_positive_review"])

# --- Chewy: one-time vs Autoship vs first-Autoship price, MAP fields. 10 credits per call.
found = client.chewy.search(query="kong classic dog toy", sort="bestselling")["data"]
print(found["redirect"])                       # set when Chewy sends the query to a category
item = client.chewy.product(product_id=found["products"][0]["product_id"])["data"]
print(item["price"], item["autoship_price"], item["first_autoship_price"], item["map_price"], item["map_enforced"])

# --- Menards: search one store (2 credits), then open a product. Prices carry
# the mail-in rebate and the final price after it. product's store_id adds that
# store's stock and aisle, costs 2 credits and can take 10-40 seconds (timeout
# raised to 120s).
store = client.menards.stores(zip="55401")["data"]["stores"][0]
hits = client.menards.search("sledge hammer", store["store_id"], sort="price_asc")["data"]
print(hits["total_results"], [(p["name"], p["final_price"], p["stock_quantity"]) for p in hits["products"][:3]])
item = client.menards.product(item_id=hits["products"][0]["item_id"], store_id=store["store_id"])["data"]
print(item["everyday_price"], item["sale_price"], item["rebates"], item["final_price"], item["you_save"])
print(item["store"]["stock_quantity"], item["store"]["locations"])
```

Whole Foods returns no ratings, reviews or UPCs. iHerb and Chewy have no store
endpoints. A Petco `store_inventory` call with one unknown `cat_entry_id` is a
404 for the whole batch.

### 27. US Retail -- Nordstrom

nordstrom.com (US site only). `search`, `category` and `brand` return 24
products a page with current and original price ranges, percent off and
on-sale flag (`category` and `brand` add the filter sidebar with product
counts); `product` lists every color and size as a sku with UPC, price, price
type and the quantity available to ship; `reviews` pages a product's full
review history with sort and filters; `availability` adds the stores that can
do in-store pickup per sku; `stores` is the store locator; `suggestions` is
the search-box autocomplete. 5 credits per call, `availability` and `reviews`
10. Every call can take several seconds, so the SDK raises their request
timeout to 120s; `reviews` takes 20-60s (up to about 100s at 200 reviews), so
its floor is 150s.

```python
from scavio import ScavioClient

client = ScavioClient()

# --- Search, deepest markdowns first. sort: relevance (default), rating,
# price_high, price_low, newest, percent_off.
found = client.nordstrom.search("dress", sort="percent_off")["data"]
print(found["total_results"], found["page_count"], found["count"])
for p in found["products"][:5]:
    print(p["style_id"], p["brand"], p["name"], p["price"], p["original_price_range"], p["percent_off"], p["badges"])

# --- A category (/browse path or URL, incl. sale/women and /browse/new) or a
# brand page: same product rows plus breadcrumbs, subcategories and filters.
cat = client.nordstrom.category("/browse/women/clothing/dresses", sort="price_low")["data"]
print(cat["category"]["title"], cat["total_results"], [s["path"] for s in cat["category"]["subcategories"][:3]])
for f in cat["filters"][:3]:
    print(f["name"], f["option_count"], [(o["label"], o["count"]) for o in f["options"][:3]])
brand = client.nordstrom.brand("/brands/astr-the-label--53360")["data"]
print(brand["brand"]["name"], brand["total_results"])

# --- One product by url or style_id: per-size UPC, price and online stock.
item = client.nordstrom.product(style_id="7737947")["data"]
print(item["price_range"], item["clearance_price_range"], item["rating"], item["review_count"])
for color in item["colors"]:
    for sku in color["skus"]:
        print(color["name"], sku["size"], sku["upc"], sku["price"], sku["price_type"], sku["in_stock"], sku["quantity"])
print(item["size_fit"]["average"], item["rating_histogram"])
for r in item["reviews"]:
    print(r["rating"], r["size_rating"], r["title"], r["verified_purchase"])

# --- Full review history (10 credits): up to 200 per call, default 60.
# sort: most_helpful (default), most_recent, highest_rated, lowest_rated.
# Filters: stars, verified_only, with_photos, search (not combinable with sort).
rev = client.nordstrom.reviews(style_id="7737947", sort="most_recent", max_reviews=100)["data"]
s = rev["summary"]
print(s["average_rating"], s["total_reviews"], s["ratings_histogram"], s["size_rating"], s["ratings_only_count"])
print([(f["name"], f["mentions"], f["quote"]) for f in s["best_features"][:3]], rev["ai_summary"])
print(rev["total_results"], rev["returned"], rev["has_more"])
for r in rev["reviews"][:5]:
    print(r["date"], r["rating"], r["title"], r["text"], r["size_purchased"], r["helpful_votes"], r["badges"], len(r["photos"]))
critical = client.nordstrom.reviews(style_id="7737947", stars=[1, 2], verified_only=True)["data"]
print(critical["total_results"], [r["text"] for r in critical["reviews"][:3]])

# --- Ship and pickup availability per sku, with the pickup stores (10 credits).
avail = client.nordstrom.availability(style_id="7737947")["data"]
print(avail["sku_count"], avail["in_stock_count"], avail["pickup_store_count"])
for sku in avail["skus"][:3]:
    print(sku["size"], sku["color"], sku["ship_quantity"], sku["pick_quantity"], [s["name"] for s in sku["pickup_stores"]])

# --- Stores near a ZIP (or latitude/longitude, or store_numbers), up to 100 miles.
for store in client.nordstrom.stores(zip="10001")["data"]["stores"][:3]:
    print(store["store_number"], store["name"], store["type"], store["distance_miles"], store["hours"], store["curbside_pickup"])

# --- Autocomplete.
print(client.nordstrom.suggestions("nike air")["data"]["suggestions"])
```

`product` reviews are the ones shown on the product page (up to about 13),
alongside the total `review_count` and `rating_histogram`; `reviews()` returns
the rest. Rating-only reviews come back with `title` and `text` null. If the
upstream page still fails after the API's own retries, the call is an unbilled
502. `quantity` and `ship_quantity` are units available to ship online;
`in_stock` is true when a sku can be shipped or picked up, so a store-only sku
reads in stock with quantity 0. `pick_quantity` is chain-wide: per store
Nordstrom only says whether pickup is available, not how many. A ZIP with no
store in range returns an empty list (billed). An unknown style id, sku id,
category or brand is a 404. For nordstromrack.com use `client.nordstrom_rack`
(next section).

### 28. US Retail -- Nordstrom Rack

nordstromrack.com (US site only), its own namespace `nordstrom_rack`, separate
from `nordstrom` but with the same methods, parameters and credit costs: 5 per
call, `availability` and `reviews` 10. `category` takes Rack's `/shop` and
`/clearance` paths, including Clear the Rack (`/clearance`) and flash events
(`/shop/flash` lists the live events as subcategories, `/shop/flash/event-N`
opens one); there is no `/browse`. `brand` takes `/brands/<slug>` with no id.
Every product row carries `clearance_price_range`, and during Clear the Rack a
clearance item can carry an extra percent off on top: `promotion_price_range`
is the price after it and `promotion_percent_off` the extra percent (all three
are null when not set). `stores` and `availability` cover Rack stores only.
Rack has its own review pool, separate from nordstrom.com's, so the same style
can show a different rating and review count on each. Same timeout floors as
`nordstrom`: 120s, `reviews` 150s (15-60s typical, up to about 100s at 200
reviews).

```python
from scavio import ScavioClient

client = ScavioClient()
rack = client.nordstrom_rack

# --- Clear the Rack: clearance listings, deepest markdowns first.
clr = rack.category("/clearance/women", sort="percent_off")["data"]
print(clr["category"]["title"], clr["total_results"], [s["path"] for s in clr["category"]["subcategories"][:3]])
for p in clr["products"][:5]:
    print(p["style_id"], p["brand"], p["name"], p["price"], p["original_price_range"],
          p["clearance_price_range"], p["promotion_price_range"], p["promotion_percent_off"])

# --- Flash events: /shop/flash lists them, each one is a listing.
events = rack.category("/shop/flash")["data"]["category"]["subcategories"]
print([(e["name"], e["path"]) for e in events[:5]])

# --- Search, a brand page, one product.
found = rack.search("dress", sort="percent_off")["data"]
print(found["total_results"], found["page_count"], found["count"])
brand = rack.brand("/brands/adidas")["data"]
print(brand["brand"]["name"], brand["total_results"])
item = rack.product(style_id="8816500")["data"]
print(item["price_range"], item["original_price_range"], item["percent_off"], item["rating"], item["review_count"])
for color in item["colors"]:
    for sku in color["skus"]:
        print(color["name"], sku["size"], sku["upc"], sku["price"], sku["price_type"], sku["in_stock"], sku["quantity"])

# --- Rack's own reviews (10 credits), same sort and filters as nordstrom.
rev = rack.reviews(style_id="7737947", max_reviews=50)["data"]
print(rev["summary"]["average_rating"], rev["summary"]["total_reviews"], rev["has_more"])

# --- In-store pickup per sku at Rack stores (10 credits), and the store locator.
avail = rack.availability(style_id="7737947")["data"]
for sku in avail["skus"][:3]:
    print(sku["size"], sku["color"], sku["ship_quantity"], sku["pick_quantity"], [s["name"] for s in sku["pickup_stores"]])
for store in rack.stores(zip="10001")["data"]["stores"][:3]:
    print(store["store_number"], store["name"], store["type"], store["distance_miles"])

print(rack.suggestions("dre")["data"]["suggestions"])
```

`pick_quantity` is chain-wide: per store the site only says whether pickup is
available, not how many. Responses carry no event start or end dates. An
unknown style id, sku id, category or brand is a 404.

### 29. US Retail -- Best Buy

bestbuy.com (US, the default), namespace `best_buy`, 9 endpoints; with
`country="ca"` the same 9 read Best Buy Canada, plus the Canada-only
`questions` (see [section 81](#81-best-buy-canada----exact-units-per-store-ehf-by-province-sale-end-dates)). US credits:
`search`, `product`, `reviews` and `prices` 2 each (`prices` is per call, up to
15 SKUs); `category` 2 for an `abcat` id and 3 for a `pcmcat` page; `deals` 3;
`stores` and `suggestions` 1; `availability` 2 flat for up to 8 stores.
`product`, `reviews` and `availability` take `sku` or `url`; `availability`
takes exactly one of `zip` or `store_ids`. `filters` is a dict: `brand`,
`on_sale`, `clearance`, `open_box`, and `min_price` with `max_price` (both
bounds). Search and category return 18 organic products per page; sponsored
tiles only with `include_sponsored=True`. Every method raises the request
timeout to at least 120s; `availability` typically takes 5-20s.

```python
from scavio import ScavioClient

client = ScavioClient()
bb = client.best_buy

# --- Search with filters, then a category listing.
found = bb.search("tv", sort="best_selling", filters={"brand": "Samsung", "on_sale": True})["data"]
print(found["total_results"], found["total_pages"], found["count"], found["sponsored_count"])
for p in found["products"][:5]:
    print(p["sku"], p["model"], p["name"], p["price"], p["regular_price"], p["savings_percent"], p["badge"])
tvs = bb.category(category_id="abcat0101001", sort="price_low")["data"]
print(tvs["category"]["name"], tvs["total_results"])

# --- One product: open-box offers by condition, UPC, specs.
item = bb.product(sku="6607832")["data"]
print(item["upc"], item["model"], item["price"], item["regular_price"], item["review_summary"])
for ob in item["open_box"]:
    print(ob["condition"], ob["price"], ob["savings_vs_new"], ob["savings_vs_regular"])

# --- Store pickup status at the stores nearest a ZIP (2 credits flat).
avail = bb.availability(sku="6607832", zip="94103", max_stores=5)["data"]
print(avail["in_stock_count"], avail["status_counts"])
for store in avail["stores"]:
    print(store["store_id"], store["name"], store["status"], store["quantity"], store["pickup_date"])

# --- Up to 15 prices in one call (2 credits), Deal of the Day, reviews.
for row in bb.prices(["6607832", "6673112", "6679316"])["data"]["prices"]:
    print(row["sku"], row["found"], row["price"], row["regular_price"], row["on_sale"])
deals = bb.deals()["data"]
print(deals["deal_of_the_day"]["name"], deals["deal_of_the_day"]["price"], deals["countdown_ends"])
rev = bb.reviews(sku="6607832", sort="newest")["data"]
print(rev["average_rating"], rev["recommended_percent"], [(c["feature"], c["mentions"]) for c in rev["pros"]])

# --- Store locator and autocomplete.
for store in bb.stores("94103")["data"]["stores"][:3]:
    print(store["store_id"], store["name"], store["distance_miles"], store["hours"][0])
print([s["term"] for s in bb.suggestions("ps5 con")["data"]["suggestions"]])
```

Availability is store pickup status, not a unit count: `quantity` is set only
for `limited` (Best Buy's "only N left") and is null for `in_stock`. Statuses
are `in_stock`, `limited`, `ship_to_store`, `out_of_stock`,
`not_available_for_pickup` and `unknown` (with a `reason`). In `prices`, a SKU
Best Buy does not know comes back `found: False`; all unknown is a 404. An
unknown SKU or category is a 404.

### 30. Trading Cards -- TCGplayer

tcgplayer.com (US marketplace, USD), namespace `tcgplayer`, 13 endpoints, 1
credit each: `search`, `product`, `listings`, `price_history`, `sales`,
`games`, `sets`, `price_guide`, `suggestions`, `trending`, `seller`,
`seller_feedback`, `seller_products`. Covers every game TCGplayer lists
(Pokemon, Magic: The Gathering, Yu-Gi-Oh!, One Piece, Lorcana and 60+ more).
`product`, `listings`, `price_history` and `sales` take `product_id` or a
tcgplayer.com `/product/<id>/` `url`. `search` needs a query unless `game` or
`set` is given. Every method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
tcg = client.tcgplayer

# --- Search a game, then one product with market price per SKU.
found = tcg.search("charizard", game="pokemon", sort="price_desc", limit=10)["data"]
print(found["total_results"], found["count"], found["has_more"])
for p in found["products"][:5]:
    print(p["product_id"], p["name"], p["set_name"], p["market_price"], p["listing_count"])

card = tcg.product(product_id=219058)["data"]
print(card["name"], card["market_price"], card["median_price"], card["seller_count"])
for sku in card["skus"]:
    # lowest/highest_sale_price and sale_count are recent SALE stats, not listings.
    print(sku["condition"], sku["printing"], sku["language"], sku["market_price"],
          sku["lowest_sale_price"], sku["highest_sale_price"], sku["sale_count"])

# --- Live offers, cheapest price plus shipping first.
offers = tcg.listings(product_id=219058, condition=["Near Mint"], limit=10)["data"]
for row in offers["listings"]:
    s = row["seller"]
    print(row["price"], row["shipping_price"], row["condition"], s["name"], s["rating_percent"])

# --- Sold volume over a month (daily buckets) and the 5 newest sales.
hist = tcg.price_history(product_id=219058, range="month")["data"]
print(hist["totals"]["quantity_sold"], hist["totals"]["transaction_count"])
for b in hist["skus"][0]["buckets"][:7]:
    print(b["date"], b["market_price"], b["quantity_sold"], b["low_sale_price"])
for sale in tcg.sales(product_id=219058)["data"]["sales"]:
    print(sale["date"], sale["condition"], sale["price"], sale["shipping_price"])

# --- Games -> sets -> a whole set's price guide.
games = tcg.games()["data"]["games"]
sets = tcg.sets("pokemon")["data"]["sets"]
guide = tcg.price_guide(604, limit=500)["data"]
print(len(games), sets[0]["set_id"], guide["set_name"], guide["total_results"])
for row in guide["rows"][:5]:
    print(row["name"], row["number"], row["condition"], row["market_price"], row["low_price"])

# --- Autocomplete, trending searches, and sellers.
print([p["name"] for p in tcg.suggestions("charizard")["data"]["products"]])
print([t["term"] for t in tcg.trending(game="pokemon")["data"]["terms"]])
seller = tcg.seller("58f7acae")["data"]
print(seller["name"], seller["rating_percent"], seller["feedback"]["total"])
fb = tcg.seller_feedback("58f7acae", rating=1, with_comment=True)["data"]
stock = tcg.seller_products("58f7acae", game="pokemon")["data"]
print(fb["total_results"], stock["total_results"])
```

`sales` returns only the 5 most recent sales (TCGplayer shows no more); use
`price_history` for sold volume, where `low_sale_price` and `high_sale_price`
are null in a bucket with no sales. Buckets are daily for `month`, 3-day for
`quarter` (default) and weekly for `semi_annual` and `annual`. Seller methods
take the 8-character `seller.key` from a listing; feedback buyers appear only
as the site's masked nickname. An unknown product id, game, set or seller key
is a 404. No store locator, product reviews or buylist prices.

### 31. Second-hand Fashion -- Vinted

Vinted on 27 country sites, namespace `vinted`, 9 endpoints, 1 credit each:
`search`, `product`, `seller`, `seller_products`, `seller_feedback`, `brands`,
`suggestions`, `filters`, `categories`. Every method takes an optional
`country`: `fr` (default), `be`, `lu`, `es`, `nl`, `lt`, `de`, `at`, `it`,
`uk`, `pt`, `us`, `cz`, `sk`, `pl`, `se`, `ro`, `hu`, `dk`, `fi`, `hr`, `gr`,
`ie`, `ee`, `lv`, `si`, `au`. Category, condition and filter names come back in
that site's language. `product` takes `item_id` or a Vinted item `url` (the
URL's own site wins). Every method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
v = client.vinted

# --- Search one country site; price is in that site's currency.
found = v.search("barbour jacket", country="uk")["data"]
print(found["listed_results"], found["total_pages"], found["total_is_capped"])
for item in found["items"][:5]:
    # service_fee is the Vinted fee the buyer pays on top of price.
    print(item["id"], item["title"], item["price"], item["currency"],
          item["service_fee"], item["total_price"], item["condition"], item["seller"]["id"])

# --- Resolve ids for filters: brands, conditions/sizes/colors, categories.
brand = v.brands("barbour", country="uk")["data"]["brands"][0]
print(brand["id"], brand["title"], brand["item_count"], brand["is_luxury"])
for opt in v.filters("status", country="uk")["data"]["options"]:
    print(opt["id"], opt["title"], opt["item_count"])
tree = v.categories(country="uk", parent_id=1904)["data"]
print(tree["parent"]["title"], [c["title"] for c in tree["categories"]][:5])
print([s["text"] for s in v.suggestions("barb", country="uk")["data"]["suggestions"]])

# --- One listing, priced in the SELLER's currency.
item = v.product(url="https://www.vinted.co.uk/items/10671938315-nike-air-max-size-uk-75")["data"]
print(item["title"], item["price"], item["currency"], item["condition"], item["is_sold"])
print(item["category"]["path"][-1]["title"], item["seller"]["login"],
      item["seller"]["feedback_reputation"])

# --- A seller: public profile, listings and reviews.
seller = v.seller(65958245, country="uk")["data"]
print(seller["login"], seller["feedback_count"], seller["feedback_reputation"], seller["item_count"])
wardrobe = v.seller_products(65958245, country="uk", limit=10)["data"]
reviews = v.seller_feedback(65958245, country="uk")["data"]
print(wardrobe["total_results"], reviews["total_results"])
for fb in reviews["feedback"][:3]:
    print(fb["rating"], fb["created_at"], fb["is_automatic"], fb["text"])
```

Every site, `uk` (GBP), `us` (USD) and `au` (AUD) included, can show listings
from sellers in other countries, with the price converted to the site's
currency (EUR, or CZK, PLN, SEK, RON, HUF, DKK on the other sites); the EU sites
share one cross-border pool. `product` returns the seller's own price and
currency, which can differ from the site's. `search` returns 96 items per page and Vinted
serves at most 10 pages (`total_is_capped` is true past 960 matches); price
sorts also surface loosely matching cheap listings, so pair them with a
category or price range. `search`'s `filters` echoes what Vinted actually
applied. Live listings only: there is no sold-item search, shipping price,
pickup point or similar-items endpoint. Seller data is limited to public,
buyer-relevant fields and feedback carries no reviewer identity. An unknown
item or member id on `product` or `seller` is a 404.

### 32. Department Store -- Macy's

macys.com (US, USD), namespace `macys`, 9 endpoints, 1 credit each: `search`,
`product`, `reviews`, `category`, `brand`, `deals`, `stores`,
`store_availability`, `suggestions`. No `country`: the US site only. `product`,
`reviews` and `store_availability` take `product_id` or a macys.com product
`url`; `category` takes `category_id` or `url`; `brand` takes `brand_id` (a
product's `brand_page_id`) or `url`. Every method raises the request timeout to
at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
m = client.macys

# --- Search: 60 organic items per page, filters from the facets.
found = m.search("jeans", brand="Levi's", special_offer="clearance", sort="price_low_to_high")["data"]
print(found["total"], found["total_pages"], found["sponsored_dropped"])
for item in found["items"][:5]:
    print(item["id"], item["title"], item["price"], item["regular_price"],
          item["percent_off"], item["sale_ends"], item["deal_label"], item["is_sponsored"])
for facet in found["facets"][:3]:
    print(facet["name"], [(v["value"], v["count"]) for v in facet["values"][:3]])

# --- Deals: sale, clearance, today_only, last_act, limited_time_special, black_friday.
clearance = m.deals(type="clearance", filters={"GENDER": "Women"})["data"]
print(clearance["label"], clearance["total"])

# --- One product (or up to 10 with product_ids, summary view).
p = m.product(product_id=25822310)["data"]
print(p["title"], p["price"], p["regular_price"], p["on_sale"], p["sale_ends"])
print(p["review_count"], p["text_review_count"], p["rating_distribution"])
for v in p["variants"][:3]:
    print(v["upc"], v["color"], v["size"], v["available"], v["availability_message"])

# --- Written reviews only (ratings without text are counted on product).
for r in m.reviews(product_id=25822310, sort="lowest_rated", limit=20)["data"]["reviews"]:
    print(r["rating"], r["date"], r["nickname"], r["title"], r["text"][:80])

# --- Store pickup: stores near a ZIP, then per-variant flags at one store.
stores = m.stores(zip="10001")["data"]["stores"]
store_id = stores[0]["store_id"]
at_store = m.store_availability(product_id=25822310, store_id=store_id)["data"]
print(at_store["pickup_available_count"], at_store["in_store_available_count"])
for v in at_store["variants"][:3]:
    print(v["upc"], v["color"], v["size"], v["pickup_available"], v["in_store_available"])
print(m.suggestions("jea")["data"]["suggestions"])
```

`search`, `category`, `brand` and `deals` share one grid: 60 organic items per
page with `total` and `total_pages`, and totals can differ between sorts, as
they do on the site. Any facet value from `facets` works in `filters`, and
`brand`, `color`, `special_offer`, `min_price` / `max_price` and
`pickup_store_id` are first-class arguments. Ad-only sponsored tiles are
dropped (`sponsored_dropped` counts them) unless `include_sponsored=True`;
organic items that also hold a paid slot stay, flagged `is_sponsored`. A
keyword Macy's maps to a category comes back with `redirected_to_category`.
A `product_ids` batch (up to 10) gets Macy's summary view: no rating histogram,
and a collection without its members' variants; a collection member's id
answers with the collection product (`requested_id` echoes the id asked for).
`review_count` includes ratings without text, `reviews` returns written reviews
only. `store_availability` takes a `store_id` (per-variant `pickup_available`
and `in_store_available`) or a location (`zip`, `lat` + `lng`, or `city` +
`state`: which stores can hand the product over), not both. Macy's publishes
no unit quantities, so there are no stock counts. No coupon codes, Q&A text or
price history: to track prices, poll and store your own.

### 33. Department Store -- Saks Fifth Avenue

saksfifthavenue.com (US, USD), namespace `saks`, 9 endpoints, 2 credits each:
`search`, `product`, `category`, `brand`, `deals`, `stores`,
`store_availability`, `suggestions`, `designers`. No `country`: the US site
only. `product` takes `product_id` (master or variant) or a product `url`;
`category` takes a `/c/` `path` or `url`; `brand` takes a designer slug (from
`designers`) or `url`; `stores` and `store_availability` take `zip` or `lat` +
`lng`. Every method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
s = client.saks

# --- Designer sale: 24 grid positions per page, filters from the facets.
sale = s.deals(type="womens_sale", brand="Prada", sort="price_low_to_high")["data"]
print(sale["label"], sale["total"], sale["total_pages"], sale["next_start"])
for item in sale["items"][:5]:
    print(item["id"], item["brand"], item["title"], item["price"],
          item["regular_price"], item["percent_off"], item["badge"])
for facet in sale["facets"][:3]:
    print(facet["id"], facet["label"], [(v["value"], v["count"]) for v in facet["values"][:3]])

# --- Walk every item: pass next_start back as start (editorial tiles can take a slot).
more = s.deals(type="womens_sale", brand="Prada", sort="price_low_to_high",
               start=sale["next_start"])["data"]
print(more["start"], more["count"], more["next_start"])

# --- Search: size takes the facet label ("Medium", not "M").
found = s.search("coat", size="Medium", on_sale=True)["data"]
print(found["total"], found["redirected_to"])

# --- One product, then one variant's pickup stock near a ZIP.
p = s.product(product_id="0400019127312")["data"]
print(p["title"], p["price"], p["on_sale"], p["is_final_sale"], p["rating"], p["review_count"])
for v in p["variants"][:3]:
    print(v["sku"], v["warehouse_units"])
near = s.store_availability(p["variants"][0]["sku"], zip="10022")["data"]
for st in near["stores"]:
    print(st["name"], st["availability_message"], st["in_stock"], st["units_at_store"])

# --- Designer index: slugs feed brand().
for d in s.designers(letter="G")["data"]["designers"][:5]:
    print(d["name"], d["slug"])
print(s.brand(brand="gucci", new_arrivals=True)["data"]["total"])
```

`search`, `category`, `brand` and `deals` share one grid: 24 positions per
page with `total`, `total_pages`, `start` and `next_start`. An editorial tile
can take a grid position, so a page may carry 22-23 items: pass the previous
`next_start` as `start` to miss nothing (`page` also works). Any facet value
from `facets` works in `filters`; `brand`, `color`, `size`, `min_price` /
`max_price`, `on_sale` and `new_arrivals` are first-class arguments, and
`size` takes the facet label ("Medium", not "M"). A keyword the site maps to a
designer or category page comes back with `redirected_to`. `deals` lists
`sale`, `womens_sale`, `mens_sale`, `womens_new_arrivals` and
`mens_new_arrivals`; Saks has no clearance or final-sale list (items carry
`is_clearance` / `is_final_sale` flags). `store_availability` needs a VARIANT
sku (a product's `variants[].sku`, or a product resolved with `color` +
`size`) and returns `units_at_store` only when the site shows a count,
otherwise null. Rating and review count only: review text is not available.
No coupon codes, international prices or price history: to track designer
sale prices, poll and store your own.

### 34. Department Store -- Kohl's

kohls.com (US, USD), namespace `kohls`, 9 endpoints, 2 credits each except
`stores` (1 credit): `search`, `product`, `category`, `brand`, `deals`,
`stores`, `store_availability`, `suggestions`, `coupons`. No `country`: the
US site only. `product` takes `product_id` or a product `url` (plus an
optional `store_id`); `category` takes a catalog `path` or `url` that carries
its `CN=` filter; `brand` takes a brand name or `url`; `stores` takes `zip`,
`city` + `state`, or `lat` + `lng`; `store_availability` takes a `sku` and a
`zip`. Every method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
k = client.kohls

# --- Clearance: 120 products per page, sponsored items kept and flagged.
clr = k.deals(type="clearance", sort="percent_off")["data"]
print(clr["label"], clr["total"], clr["total_pages"], clr["sponsored_count"])
for item in clr["items"][:5]:
    print(item["id"], item["title"], item["price"], item["regular_price"],
          item["price_label"], item["percent_off"], item["with_code_price"],
          item["with_code_offer_codes"], item["is_sponsored"])

# --- Facet value ids feed filters (price is a bucket, not a free min / max).
for facet in clr["facets"][:3]:
    print(facet["id"], facet["label"], [(v["value"], v["count"]) for v in facet["values"][:3]])
found = k.search("jeans", brand="Levi's", filters=["Gender:Womens", "Price:$25 to $50"])["data"]
print(found["total"], found["corrected_query"])

# --- One product, then one variant's pickup units near a ZIP.
p = k.product(product_id="6251213")["data"]
print(p["title"], p["price"], p["regular_price"], p["rating"], p["review_count"], p["dept"])
print(p["kohls_cash"], [(o["code"], o["ends"]) for o in p["offers"]])
v = p["variants"][0]
print(v["sku"], v["upc"], v["color"], v["size"], v["online_units"])
near = k.store_availability(v["sku"], "10001", dept=p["dept"])["data"]
print(near["in_stock_count"], near["total_pickup_units"])
for st in near["stores"][:5]:
    print(st["name"], st["pickup_units"], st["stock_level"], st["distance_miles"])

# --- Stores, then today's public coupon codes.
for st in k.stores(zip="60601")["data"]["stores"][:3]:
    print(st["store_id"], st["name"], st["city"], st["badges"])
for c in k.coupons()["data"]["offers"]:
    print(c["code"], c["description"], c["ends"], c["requires_kohls_card"])
```

`search`, `category`, `brand` and `deals` share one grid: 120 products per
page with `total` and `total_pages`. Up to about 8 sponsored items stay in the
list, flagged `is_sponsored` and counted in `sponsored_count`. Any facet value
id from `facets` works in `filters` (one id or a list, combined with AND);
`brand`, `color`, `size`, `on_sale` and `clearance` are first-class
arguments. Price is a facet bucket ("Price:$25 to $50"), not a free min /
max. Search returns `corrected_query` when the site autocorrects a keyword.
`deals` lists `clearance` (default), `sale`, `kohls_cash` (items that earn
Kohl's Cash now) and `sephora` (Sephora at Kohl's). Prices carry
`price_label` (sale, clearance, clearance+regular), `percent_off`,
`with_code_price` (the price after a public offer code, with the code) and
`price_suppressed` + `price_note` for cart-only prices. `store_availability`
takes a product's `variants[].sku` (and optionally its `dept`) and returns
real pickup unit counts at every store within about 50 miles of the ZIP.
Rating and review count only: review text is not available. No price
history, international sites, account offers or checkout: to track
clearance prices, poll and store your own.

### 35. Department Store -- JCPenney

jcpenney.com (US incl. Puerto Rico stores, USD), namespace `jcpenney`, 11
endpoints, 1 credit each: `search`, `product`, `category`, `brand`, `deals`,
`stores`, `store_availability`, `suggestions`, `coupons`, `reviews`,
`questions`. No `country`: the US site only. `product` takes `product_id`, a product `url` or up to 20
`product_ids`; `category` takes a `/g/` `path` or `url` that carries its
`id=cat...`; `brand` takes a brand name or `url`; `stores` takes `zip`,
`city` + `state`, or `lat` + `lng`; `store_availability` takes a `sku` plus
`zip` (or `lat` + `lng`); `reviews` and `questions` take `product_id` or a
product `url`. Every method raises the request timeout to at least 120s;
`reviews` and `questions` raise it to 240s.

```python
from scavio import ScavioClient

client = ScavioClient()
j = client.jcpenney

# --- Clearance: 48 products per page, at most 25 pages.
clr = j.deals(type="clearance")["data"]
print(clr["type"], clr["total"], clr["total_pages"])
for item in clr["items"][:5]:
    print(item["id"], item["title"], item["price"], item["price_max"],
          item["regular_price"], item["price_type"], item["percent_off"],
          item["coupon_price"], item["coupon_code"])

# --- Facet values feed filters as {facet id: value}.
for facet in clr["facets"][:3]:
    print(facet["id"], facet["label"], [(v["value"], v["count"]) for v in facet["values"][:3]])
found = j.search("jeans", brand="levi's", filters={"gender": "women"})["data"]
print(found["total"], found["corrected_query"], found["redirected_to"])

# --- One product (product-level price ranges), then one variant's units
# --- at the 5 nearest stores.
p = j.product(product_id="ppr5008604049")["data"]
price = p["price"]
print(p["title"], price["current_min"], price["current_max"], price["regular_min"],
      price["price_type"], price["coupon"], p["rating"], p["review_count"])
v = p["variants"][0]
print(v["sku"], v["upc"], v["color"], v["size"], v["online_stock"])
near = j.store_availability(v["sku"], zip="90012")["data"]
print(near["stores_with_stock"], near["total_quantity"])
for st in near["stores"]:
    print(st["name"], st["quantity"], st["status"], st["distance_miles"])

# --- Stores, then today's public coupon codes.
for st in j.stores(zip="75024")["data"]["stores"][:3]:
    print(st["store_id"], st["name"], st["city"], st["services"])
for c in j.coupons()["data"]["coupons"]:
    print(c["code"], c["channel"], c["headline"], c["ends_at"])

# --- Review text (slow: usually 15-90s, up to about 3 minutes).
rv = j.reviews(product_id="ppr5008604049", sort="most_helpful")["data"]
print(rv["total_reviews"], rv["displayed_reviews"], rv["matching_reviews"],
      rv["average_rating"], rv["rating_distribution"], rv["recommended_percent"])
for r in rv["reviews"][:3]:
    print(r["rating"], r["title"], r["author"], r["submitted_at"],
          r["helpful_votes"], r["verified_purchaser"], r["incentivized"], r["syndicated"])

# --- Questions and every answer, with who answered.
qa = j.questions(product_id="ppr5008212471")["data"]
print(qa["total_questions"], qa["total_answers"])
for q in qa["questions"][:3]:
    print(q["question"], q["answer_count"])
    for a in q["answers"]:
        print("  ", a["author_type"], a["ai_label"], a["text"][:80])
```

`search`, `category`, `brand` and `deals` share one grid: 48 products per
page, at most 25 pages (1,200 items deep), with `total` and `total_pages`.
Any facet from `facets` works in `filters` as `{facets[].id: value}` (one
value or a list, facets combined with AND); `brand`, `color`, `size`,
`price_range` and `deal` (a Deals & Promotions label) are first-class
arguments, each one value or a list. Search returns `corrected_query` when
the site autocorrects a keyword and `redirected_to` when it sends a keyword
(doorbusters) to a deal or category listing; `exact=True` skips the
automatic category narrowing. `deals` lists `clearance` (default), `sale`,
`black_friday`, `big_buy`, `limited_time_special`, `best_value`,
`gotta_have_it`, `closeout` and `bogo`, or any `label` verbatim, across all
products or one `department`. Prices are product-level ranges (regular,
sale and clearance min / max, `percent_off`, `price_type`) plus the
after-coupon price and its code: JCPenney does not expose a price per size
or color. Variants carry an online stock level (high / low / out), not a
count. `store_availability` takes a product's `variants[].sku` and returns
real unit counts at the 5 nearest stores. `reviews` returns up to 98 review
texts (default 38), sorted `most_recent` (default), `most_helpful`,
`highest_rating`, `lowest_rating` or `relevance`, optionally one star
`rating`; `total_reviews` counts every language, `displayed_reviews` the
English reviews JCPenney lists, `matching_reviews` those under the sort and
filter. Each review carries `verified_purchaser`, `incentivized`,
`syndicated` with `syndication_source`, photos, videos, secondary ratings
(Quality, Value...) and the brand's response. `questions` returns up to 50
questions (default 10, no sort option) with every answer's `author_type`
(`brand`, `retailer` for JCPenney staff, `ai`, `customer`) and `ai_label`
(AI-Generated / AI-Assisted). Both are slower than the other endpoints
(usually 15-90s, up to about 3 minutes) and failed calls are not charged.
Reviewer age, gender and IP addresses are never returned. No price history,
international sites, account offers or JCPenney Rewards balances, or
checkout: to track clearance prices, poll and store your own.

### 36. Sporting Goods -- Dick's Sporting Goods

dickssportinggoods.com (US, USD), namespace `dicks`, 9 endpoints, 1 credit
each except `product` and `reviews` (2 credits): `search`, `product`,
`products`, `reviews`, `category`, `brand`, `deals`, `store_availability`,
`suggestions`. No `country`: the US site only. `product` and `reviews` take
`product_id` or a product `url`; `products` takes up to 5 `product_ids`;
`category` takes a `/f/` or `/c/` `path`, a `url` or a `category_id`;
`store_availability` takes a list of `skus` plus `zip` (or `lat` + `lng`).
Every method raises the request timeout to at least 120s; `product` and
`reviews` raise it to 240s (usually 20-75s, up to about 2.5 minutes).

```python
from scavio import ScavioClient

client = ScavioClient()
d = client.dicks

# --- Clearance: 48 items per page by default, up to 144.
clr = d.deals(type="clearance", sort="savings")["data"]
print(clr["label"], clr["total"], clr["total_pages"])
for item in clr["items"][:5]:
    print(item["id"], item["title"], item["price"], item["price_max"],
          item["list_price"], item["percent_off"], item["is_pinned"],
          item["scheduled_prices"])

# --- Facet values feed filters as {facet id: value}.
for facet in clr["facets"][:3]:
    print(facet["id"], facet["label"], [(v["value"], v["count"]) for v in facet["values"][:3]])
found = d.search("running shoes", brand="HOKA", filters={"5495": "Men's"})["data"]
print(found["total"], found["did_you_mean"], found["redirected_to"])

# --- One product: prices differ per SKU (size / color), then store units.
p = d.product(product_id="23FHQMCLFTN9GTXBLMNS")["data"]
print(p["title"], p["price"]["min"], p["price"]["max"], p["is_clearance"])
for v in p["variants"][:5]:
    print(v["sku"], v["color"], v["size"], v["price"], v["list_price"],
          v["is_clearance"], v["online_units"])
skus = [v["sku"] for v in p["variants"][:2]]
near = d.store_availability(skus, zip="60601")["data"]
print(near["stores_with_stock"], near["sku_totals"])
for st in near["stores"][:3]:
    print(st["name"], st["distance_miles"], [(s["sku"], s["units"]) for s in st["skus"]])

# --- The 15 newest reviews plus rating stats.
r = d.reviews(product_id="26UNDMFITN1HRI9WUAETC")["data"]
print(r["stats"]["total"], r["stats"]["average"], r["stats"]["distribution"])
for rev in r["reviews"][:3]:
    print(rev["rating"], rev["title"], rev["submitted_at"])
```

`search`, `category`, `brand` and `deals` share one grid: 48 items per page
by default, up to 144 (`page_size`), with `total` and `total_pages`, sorted
by `relevance`, `top_sellers`, `savings`, `price_low_to_high`,
`price_high_to_low`, `featured`, `new_arrivals` or `brand_az`. Any facet
from `facets` works in `filters` as `{facets[].id: value}` (one value or a
list, facets combined with AND); `min_price` / `max_price` are approximate.
Merchandised items are flagged `is_pinned` and can make page 1 a few items
longer than `page_size`. Search returns `did_you_mean` for a misspelled
query and follows keywords Dick's sends to a landing page (`clearance`,
`golf balls`), reported as `redirected_to`. `scheduled_prices` are the
retailer's own planned offer-price windows and can change: not a forecast
or price history. `deals` lists `clearance` (default), `sale` or
`weekly_deals`. Prices differ per size and color, so `product` lists every
SKU with its own price, list price, `is_clearance`, `online_units`, UPC and
`buyable` flag; `products` is the cheap style-level summary for up to 5
ids. `reviews` returns the 15 newest reviews with full text and the rating
stats: no paging, sort or star filter, and questions and answers are counts
only. `store_availability` takes SKUs from `product` and returns unit counts
at up to 100 DICK'S, Golf Galaxy (`chain="golf_galaxy"`) or Public Lands
(`chain="public_lands"`) stores, with each store's address, phone, hours and
distance; there is no standalone store locator, and an unknown SKU reads 0
everywhere. No price history, ScoreCard prices or points, international
sites, account data or checkout: to track clearance prices, poll and store
your own.

### 37. Sneakers -- Foot Locker

Foot Locker, namespace `footlocker`, 10 endpoints, 1 credit each: `search`,
`product`, `category`, `brand`, `deals`, `releases`, `stores`,
`store_availability`, `reviews`, `questions`. `country` picks the
storefront: `us` (footlocker.com, USD, default), `ca` (CAD, `language` en
or fr), `gb` (GBP), `de`, `fr`, `it`, `es`, `nl`, `be` (`language` nl or
fr), `at`, `ie` (EUR), `au` (AUD) or `nz` (NZD); titles come in the
storefront's language. Search, product, category, brand and deals (`sale`,
`discount_eligible`) work on all 13; `exclusives` on us and ca; `releases`
on us, ca and gb (gb has no prices or reservation windows); `stores`,
`store_availability`, `reviews` and `questions` are US only. Every method
raises the request timeout to at least 120s; `reviews` and `questions`
raise it to 240s (usually 25-90s, up to about 3-4 minutes).

```python
from scavio import ScavioClient

client = ScavioClient()
fl = client.footlocker

# --- Search: 48 items per page, any storefront, data_as_of on every listing.
res = fl.search("nike dunk", country="de", sort="price_low_to_high")["data"]
print(res["currency"], res["total"], res["total_pages"], res["data_as_of"], res["redirected_to"])
for item in res["items"][:5]:
    print(item["id"], item["title"], item["price"], item["list_price"],
          item["percent_off"], item["lowest_price_30d"])

# --- Facet values feed filters as {facet id: value}.
for facet in res["facets"][:3]:
    print(facet["id"], facet["label"], [(v["value"], v["count"]) for v in facet["values"][:3]])
mens10 = fl.brand(brand="New Balance", filters={"mensShoesSize": "10.0"})["data"]
print(mens10["brand"], mens10["total"])

# --- One product: availability is yes / no per size, never unit counts.
p = fl.product(product_id="Q5495005")["data"]
print(p["title"], p["price"], p["launch"])
for size in p["sizes"][:5]:
    print(size["size"], size["available"], size["ship"], size["pickup"],
          size["stores_available"])

# --- Which nearby stores show size 10.0 as available (US).
near = fl.store_availability(product_id="W2288111", size="10.0", zip="10001")["data"]
print(near["stores_with_availability"])
for st in near["stores"][:3]:
    print(st["name_secondary"], st["distance_miles"], st["available"], st["sizes_available"])

# --- The release calendar: monitoring data only.
cal = fl.releases(status="upcoming", brand="Jordan")["data"]
for r in cal["releases"][:5]:
    print(r["launch_at"], r["title"], r["style"], r["retail_price"], r["heat_level"],
          r["reservation"]["status"])

# --- Reviews (slow): 1-98 with full text, sort and star filter.
rv = fl.reviews(product_id="Q5495005", sort="most_helpful", limit=30)["data"]
print(rv["stats"]["average_rating"], rv["stats"]["rating_distribution"])
for review in rv["reviews"][:3]:
    print(review["rating"], review["title"], review["submitted_at"])
```

`search`, `category`, `brand` and `deals` share one grid: 48 items per page
with `total` and `total_pages`, sorted by `relevance`, `price_low_to_high`,
`price_high_to_low`, `new_arrivals`, `top_rated`, `name_az` or `brand_az`.
Filter by `brand` (any case), `gender`, `color`, `price_range`, `on_sale`,
or any facet from `facets` via `filters` as `{facets[].id: value}` (one
value or a list, filters combined with AND). Listings can be a few hours
old: `data_as_of` says when each one was built. A bare brand keyword
(`nike`, `hoka`) is answered with that brand's listing and reported as
`redirected_to`; a keyword the site sends to a landing page without a
product listing is an unbilled 400 pointing to `brand`, `category` or
`deals`. `product` lists every colorway with its price and every size with
`available`, `ship`, `pickup` and `stores_available` (how many stores show
the size as available: a store count, not units); European storefronts add
`lowest_price_30d`. `releases` is the release calendar as monitoring data:
launch date and time, retail price, colorway, style code, heat level, size
run and reservation windows where the storefront runs them; nothing here
enters, reserves or buys a release. `store_availability` covers Foot Locker
banner stores only (no Kids Foot Locker or Champs) and answers yes / no.
Unknown SKUs, categories and brands are a charged 404. No search
suggestions, member (FLX) prices or account data, price history or
checkout: to track prices, poll and store your own.

### 38. Fan Merchandise -- Fanatics

Fanatics merchandise and product data (jerseys, hats, fan gear,
collectibles; not sportsbook odds), namespace `fanatics`, 5 endpoints, 1
credit each: `search`, `product`, `browse`, `deals`, `reviews`. `country`
picks the storefront: `us` (fanatics.com, USD, default), `gb` (GBP), `de`,
`fr`, `es`, `it` (EUR), `jp` (JPY) or `ca` (CAD, `language` en or fr);
titles come in the storefront's language. `site` reads a US league store
(with country us): `fanatics` (default), `nflshop`, `mlbshop`, `nhlshop` or
`mlsstore`; the same product ids work on every store, but department and
filter ids are per store (Jerseys is 8011 on fanatics.com, 14012 on NFL
Shop): take them from the facets of the store you query. `search`, `product`,
`browse` and `deals` take both; `reviews` is US only (fanatics.com). Every
method raises the request timeout to at least 120s; `reviews` raises it to
300s (usually 20-90s, up to about 4 minutes).

```python
from scavio import ScavioClient

client = ScavioClient()
fan = client.fanatics

# --- Search: up to 72 items per page, data_as_of on every listing.
res = fan.search("chiefs jersey", sort="price_low_to_high")["data"]
print(res["total"], res["total_capped"], res["corrected_query"], res["data_as_of"])
for item in res["items"][:5]:
    print(item["id"], item["title"], item["price"], item["regular_price"],
          item["with_code_price"], item["price_label"], item["ship_by"])

# --- Facet values feed filters as {filter: value}; ids feed browse().
for facet in res["facets"][:3]:
    print(facet["id"], facet["label"], [(v["label"], v["filter"], v["value"]) for v in facet["values"][:3]])

# --- A team's hats, or a league store (NFL Shop): same product ids, its own department ids.
hats = fan.browse(team_id=3372, department_id=8008, price_band="25_50")["data"]
print(hats["browse"]["team"], hats["browse"]["department"], hats["total"])
nfl = fan.search("mahomes jersey", site="nflshop")["data"]
print(nfl["site"], nfl["total"])

# --- One product: regular / sale / clearance / with-code price, stock level per size.
p = fan.product(product_id="3892922")["data"]
print(p["title"], p["price"], p["sale_price"], p["clearance_price"], p["with_code_price"])
print(p["coupon"], p["flags"], p["customizable"], p["personalization"])
for size in p["sizes"]:
    print(size["size"], size["available"], size["stock_level"], size["ship_by"],
          size["est_delivery_from"], size["est_delivery_to"])

# --- Sale and clearance listings, other storefronts in local currency.
sale = fan.deals(type="clearance", league_id=25)["data"]
print(sale["count"], sale["total"])
de = fan.deals(country="de")["data"]
print(de["currency"], de["total"], de["data_as_of"])

# --- Reviews (slow): style rollup, so each review names its product.
rv = fan.reviews(product_id="3892922", sort="most_recent", limit=30)["data"]
print(rv["stats"]["average"], rv["stats"]["fit"], rv["ai_summary"])
for review in rv["reviews"][:3]:
    print(review["product_id"], review["rating"], review["fit"], review["text"])
```

`search`, `browse` and `deals` share one grid: 24, 48 or 72 items per page
(default 72) with `total`, `total_capped` (the US site counts at most 9000)
and `total_pages`, sorted by `top_sellers`, `price_low_to_high`,
`price_high_to_low` or `newest` (price sorts use the current `price`, before
any promo code, not `with_code_price`). Each item carries `price`,
`regular_price`, `sale_price`, `clearance_price`, `with_code_price` (the
price with the site-wide promo code shown on the page) and `price_label`
(`coupon` means coupon-eligible; a null `with_code_price` means the code does
not lower that item). Player ids come from the players facet when the page
lists one (e.g. Lakers) or from a product's `player`.
Filter by `gender`, ids (`league_id`, `team_id`, `player_id`,
`department_id`, `brand_id`, `collection_id`; `browse` and `deals`) or any
facet value via `filters` as `{filter: value}`, one value per filter;
`price_band` and `on_sale` are on `browse` (price bands are not on jp). A
league alone is a landing page: combine it with another id or a filter.
`data_as_of` says when Fanatics built each listing; misspellings come back
as `corrected_query`. `product` lists every size with `stock_level` (low /
out: a level, never a unit count), ship-by and delivery estimates, the
current promo code, personalization fields with the team roster (prices
already include personalization), and jersey assurance / authentic flags.
`reviews` returns real text with 4 sorts and a star filter (1-50, default
10), fit / quality / value, and the site's own AI-written summary
(`ai_summary`); Fanatics pools reviews across a style, so check each
review's `product_id`. Unknown products are a charged 404. No search
suggestions, store locator or store stock, Q&A, FanCash, member pricing,
unit counts, price history or checkout: to track jersey sale prices, poll
and store your own.

### 39. Grocery -- Carrefour

Carrefour grocery prices by store, promotions, Nutri-Score and stores,
namespace `carrefour`, 9 endpoints, 1 credit each: `search`, `product`,
`reviews`, `category`, `promotions`, `suggestions`, `stores`,
`store_availability`, `store`. carrefour.fr (France) serves every endpoint;
`search` and `product` also take `country` `ar` (Argentina, ARS), `ro`
(Romania, RON) or `be` (Belgium, EUR, `language` fr or nl; 2 credits). Data
comes back in the market's language: French titles, labels and ingredients
on fr. Without `store` a price is carrefour.fr's national online price; pass
a store ref from `stores()` (`store_ref` or `pickup_refs[].ref`) or
`store_availability()` (`stores[].store.ref`) for that store's shelf price
and assortment. Every method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
cf = client.carrefour

# --- Search: national online price, unit price, promotion, Nutri-Score.
res = cf.search("nutella")["data"]
print(res["total"], res["store"], res["price_scope"], res["currency"])
for item in res["items"][:5]:
    print(item["ean"], item["title"], item["price"], item["unit_price_label"],
          item["nutriscore"], item["promotion"])

# --- Stores near a postal code; a store ref scopes prices to that store.
stores = cf.stores(postal_code="69003")["data"]["stores"]
for s in stores[:3]:
    print(s["store_ref"], s["name"], s["banner"], s["distance_km"], s["slug"])
local = cf.search("nutella", store="840093")["data"]
print(local["store"], local["price_scope"], local["total"])

# --- One product: ingredients, allergens, nutrition per 100 g, rating.
p = cf.product(ean="3017620422003")["data"]
print(p["title"], p["price"], p["unit_price"], p["unit"], p["ecoscore"])
print(p["ingredients"], p["allergens"])
for row in p["nutrition"]["per_100"]["values"]:
    print(row["nutrient"], row["quantity"])

# --- Promotions: catalogue, immediate, loyalty-card (member) or festive.
promo = cf.promotions(type="loyalty", category="Boissons")["data"]
for item in promo["items"][:3]:
    d = item["promotion"]
    print(item["title"], d["label"], d["loyalty_only"], d["discounted_price"],
          d["initial_price"], d["ends_at"])

# --- Which nearby stores carry a product (yes / no, no price), store detail with fuel.
av = cf.store_availability("3017620422003", "69003")["data"]
print(av["available_count"], [(s["store"]["ref"], s["available"]) for s in av["stores"][:3]])
st = cf.store(slug="venissieux")["data"]
print(st["store"]["name"], st["store"]["next_slots"])
if st["fuel"]:
    for f in st["fuel"]["prices"]:
        print(f["fuel"], f["price_per_litre"], f["updated_at"])

# --- Verified-purchase reviews, and other markets (search / product only).
rv = cf.reviews("8006530256179", sort="lowest_rated", limit=20)["data"]
print(rv["total"], [(r["author"], r["rating"], r["text"]) for r in rv["reviews"][:2]])
be = cf.search("chocolat", country="be", language="nl")["data"]
print(be["country"], be["language"], be["currency"], be["total"])
```

`search`, `category` and `promotions` share one grid (30 items per page on
fr; ar and ro 24, be 36) with `total`, `total_pages` and every facet; filter
by `brand`, `promotion`, `nutriscore`, `organic`, `carrefour_brands` or
`min_price` / `max_price`, and sort by `relevance`, `price_low_to_high`,
`price_high_to_low`, `unit_price_low_to_high`, `unit_price_high_to_low` or
`top_rated` (ar and ro: relevance and the price sorts; be: relevance). Each
item carries `price`, `unit_price` with `unit_price_label` (per kg / L),
`nutriscore`, `ecoscore` and `promotion` (`type`, `label`, `loyalty_only` for
loyalty-card prices, `discounted_price`, `initial_price`, `quantity`,
`starts_at`, `ends_at`). On multi-buy deals ("Le 2ème à -50%") the prices
cover `quantity` items and `discounted_price` is None when the site does not
price the deal. Store prices differ from national ones (Nutella 400 g: 3.99
national, 3.69 at two stores, 4.61 at another). `reviews` returns 1-50
verified-purchase reviews (default 10) with 4 sorts, a star filter and
`offset` paging; authors appear as published (first name and last initial).
`stores` finds stores by postal code or `lat` / `lng`, optionally with one
`service` (`drive`, `station_service`...). `store` returns services, weekly
hours, drive hours, the next pickup slots as shown and, at stores with a fuel
station, fuel prices per litre with update times. Failed calls are not
charged; a not-found is a charged 404. No Q&A, printed leaflet,
delivery-slot booking, cart, loyalty account data or price history: to track
prices, poll and store your own. Spain, Italy, Poland, Brazil and the Middle
East sites are not covered.

### 40. Marketplace -- Allegro

Allegro offers, every seller's price for one product, sellers and seller
feedback, namespace `allegro`, 7 endpoints, 2 credits each: `search`,
`offer`, `product`, `product_offers`, `seller`, `seller_feedback`,
`category`. Every endpoint takes `country`: `pl` (allegro.pl, PLN, default),
`cz` (allegro.cz, CZK), `sk` (allegro.sk, EUR) or `hu` (allegro.hu, HUF).
Titles, parameters and labels come back in the site's language (Polish on
pl). An offer is one seller's listing (`offer_id`); a catalogue product
(`product_id`) groups many sellers' offers, and `product_offers()` lists every
seller's price for it. sk and hu calls can take up to about a minute; every
method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
al = client.allegro

# --- Search: price, price with delivery, sold count, seller, sponsored flag.
res = al.search("laptop", sort="price_low_to_high", condition="new")["data"]
print(res["total"], res["total_pages"], res["currency"], res["language"])
for item in res["items"][:5]:
    print(item["offer_id"], item["title"], item["price"], item["price_with_delivery"],
          item["sold_count"], item["seller"]["login"], item["placement"])

# --- One offer: 30-day lowest price on a discount, stock, delivery, seller.
o = al.offer(offer_id="18801787032")["data"]
print(o["price"], o["original_price"], o["lowest_price_30d"], o["discount_percent"])
print(o["stock"], o["sold_count"], o["seller"]["login"], o["seller"]["company_name"])
for d in o["delivery"][:3]:
    print(d["method"], d["price"], d["eta_text"])

# --- A catalogue product, then every seller's offer for it (price monitoring).
p = al.product(product_id="90d08230-e02a-4210-913d-d417453321b8")["data"]
print(p["title"], p["lowest_price"], p["offer_count"], p["rating"]["average"])
print(p["featured_offer"]["price"], p["featured_offer"]["seller"]["login"])
for r in p["reviews"][:3]:
    print(r["rating"], r["author"], r["text"])
offers = al.product_offers(product_id=p["product_id"],
                           sort="price_with_delivery_low_to_high")["data"]
for of in offers["offers"][:5]:
    print(of["seller"]["login"], of["price"], of["price_with_delivery"],
          of["smart"], of["is_featured"])

# --- A seller's offers, then the seller's feedback score.
s = al.seller("Yupilo_pl", query="lenovo", category="komputery")["data"]
print(s["seller"]["is_business"], [(c["name"], c["slug"]) for c in s["categories"]])
fb = al.seller_feedback("Yupilo_pl")["data"]
print(fb["summary"]["positive_percent"], fb["summary"]["super_seller"],
      fb["summary"]["member_since"])

# --- A category, and another market (Hungarian titles, HUF prices).
cat = al.category(category_id=491, sort="popularity")["data"]
print(cat["category"]["name"], cat["category"]["breadcrumb"], cat["total"])
hu = al.search("laptop", country="hu")["data"]
print(hu["currency"], hu["items"][0]["title"], hu["items"][0]["price"])
```

`search`, `category` and `seller` share one grid: 60 organic offers per page
(sponsored slots on top), up to 100 pages, exact `total` and every facet.
Sort by `relevance`, `price_low_to_high`, `price_high_to_low`,
`price_with_delivery_low_to_high`, `price_with_delivery_high_to_low`,
`popularity`, `ending_soonest` or `newest`; filter by `min_price` /
`max_price`, `condition` (`new` / `used`), `smart`, and on pl only
`buying_format` (`buy_now` / `auction`) and `deals` (Allegro's deals zone,
Black Weeks included while it runs); both pl-only filters are a 400
elsewhere. Each item carries `price`, `price_with_delivery`, `condition`,
`is_auction`, `discount_percent` and `lowest_price_30d`, the seller
(`super_seller`, `positive_feedback_percent`, `is_business`), `sold_count`,
`smart`, `placement` (regular, promoted, sponsored or featured) and `source`
(`allegro_lokalnie` for Allegro Lokalnie offers inside pl results).
`lowest_price_30d` is the EU disclosure Allegro shows next to a discount (the
lowest price in the 30 days before it): None without a discount, and not a
price history. `sold_count` is None on auctions and on cz, sk and hu offer
pages. `offer` returns the auction state (current price, minimum next bid,
ends at, has bids; no bid history), every parameter with GTIN and brand,
delivery methods, returns, warranty and `company_name` for business sellers.
`product` returns `lowest_price`, `offer_count`, the featured (buy box) offer,
the star distribution, review aspects and the first 20 reviews as shown on
the page. `seller` returns id, login, `is_business` and the seller's
categories (`slug` feeds `category`); super seller status, positive percent
and member since come from `seller_feedback` (20 ratings per page, no buyer
identity). Failed calls are not charged; a not-found is a charged 404. No
search suggestions, bidding, buying or checkout, Allegro Lokalnie as its own
source, Smart! account data, seller revenue, seller addresses or tax ids,
price history or reviews past the first 20: to track prices, poll and store
your own.

### 41. Lead Enrichment -- `company.enrich()`

Turn a business website or a Google Maps place_id into contact data,
namespace `company`, 1 endpoint: `enrich(url=None, place_id=None)`. Provide
`url` or `place_id`; one of the two is required (the SDK raises
`ScavioError` before sending when both are missing). Returns the company's
published emails, phone numbers (E.164), social profiles and contact
page, plus the owner or founder's name and title with the page that names
them. 10 credits from a `url`, 20 from a `place_id` (1 when the listing has no
readable website); a website that cannot be reached is not charged, and
`credits_used` in the response is the exact charge. A call reads several pages
and usually takes 10-45s, but a slow site can take about 2 minutes, so
`enrich()` raises the request timeout to at least 180s.

```python
from scavio import ScavioClient

client = ScavioClient()

# --- From a website (10 credits). A bare domain works.
res = client.company.enrich("https://reliantplumbing.com")
co = res["data"]["company"]
print(co["name"], co["domain"], co["emails"], co["phones"])
print(co["socials"].get("facebook"), co["contact_page"])
owner = res["data"]["owner"]  # None when no page names an owner
if owner:
    print(owner["name"], owner["title"], owner["source_url"],
          owner["email"], owner["email_status"])
print(res["credits_used"])

# --- After a Google Maps search: enrich each result by place_id (20 credits).
places = client.google.maps_search("plumbers in Austin")["local_results"]
for place in places[:3]:
    lead = client.company.enrich(place_id=place["place_id"])["data"]
    print(lead["company"]["name"], lead["company"]["website"],
          lead["company"]["emails"], lead["company"]["phones"])
```

`socials` keys are `facebook`, `instagram`, `linkedin`, `x`, `tiktok`,
`youtube` and `pinterest`, present only when found. `owner.email_status` is
`published` when an address on the site matches the owner's name, otherwise
`not_found` with `owner.email` None. Each call reads the home page, up to 3
contact, about or team pages, and the privacy and terms pages. Social profile
links (Facebook, Instagram, LinkedIn...) are rejected as `url` with a 400: pass
the business's own site. When both `url` and `place_id` are sent, `url` is the
site that gets read.

### 42. Classifieds -- OLX

OLX Europe classifieds (used goods, cars, real estate, jobs), namespace
`olx`, 9 endpoints, 1 credit each: `search`, `offer`, `seller`,
`seller_ads`, `filters`, `categories`, `locations`, `suggestions`,
`similar`. OLX Europe only: `country` is `pl` (olx.pl, PLN, default), `ro`
(olx.ro, RON), `pt` (olx.pt, EUR), `bg` (olx.bg, EUR), `ua` (olx.ua, UAH),
`kz` (olx.kz, KZT) or `uz` (olx.uz, UZS); `filters` and `similar` are pl, ro,
pt, bg and ua only. OLX Brasil, olx.in and other OLX-branded sites are not
covered. Titles, params and labels come back in the site's language (Polish
on pl; Russian by default on kz and uz, `language="kk"` / `"uz"` for Kazakh
or Uzbek on `search`, `seller_ads` and `offer`). Every method raises the
request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
olx = client.olx

# --- Search: promoted ads are interleaved and flagged; 1,000-result cap.
res = olx.search(query="iphone", sort="newest", seller_type="private")["data"]
print(res["total"], res["total_capped"], res["promoted_count"], res["currency"])
for item in res["items"][:5]:
    print(item["id"], item["title"], item["price"]["value"], item["condition"],
          item["location"]["city"], item["refreshed_at"], item["is_promoted"])

# --- Discover a category's filters, then search with them.
f = olx.filters(84)["data"]
for flt in f["filters"][:5]:
    print(flt["key"], flt["label"], flt["kind"], flt["send_as"])
cars = olx.search(category_id=84, filters={"filter_float_year:from": 2018,
                                           "filter_float_milage:to": 100000})["data"]

# --- Places and categories for the location and category filters.
loc = olx.locations("Warszawa")["data"]["locations"][0]
print(loc["city"], loc["city_id"], loc["region_id"])
near = olx.search(query="rower", city_id=loc["city_id"], distance_km=30)["data"]
top = olx.categories()["data"]["categories"]
print([(c["id"], c["name"], c["count"]) for c in top[:5]])

# --- One ad, its seller, the seller's ads and similar ads.
ad = olx.offer(offer_id="1107557408")["data"]
print(ad["title"], ad["price"], ad["category"]["breadcrumb"], ad["seller"])
s = olx.seller(2547532895)["data"]
print(s["is_business"], s["business_name"], s["member_since"], s["active_ads"])
ads = olx.seller_ads(2547532895, sort="price_low_to_high")["data"]
sim = olx.similar(offer_id="1107557408")["data"]
print(ads["total"], sim["count"])

# --- olx.uz: Russian titles by default; y.e. prices come converted to UZS.
uz = olx.search(query="iphone", country="uz")["data"]
for item in uz["items"]:
    p = item["price"]
    if p["original_currency"]:  # e.g. 529 UYE -> 6334404.7 UZS
        print(p["value"], p["currency"], p["original_value"], p["original_currency"])
```

`search` and `seller_ads` share one grid: up to 50 ads per page (default 40;
promoted ads come on top, each flagged `is_promoted` with
`promoted_position`, `include_promoted=False` drops them), and OLX lets
anyone page through the first 1,000 results only (`total_capped`; kz and uz
hide large totals, so `total` is None there). Sort by `relevance`, `newest`
(last refresh, not first posting: sellers can refresh an ad),
`price_low_to_high` or `price_high_to_low`; filter by `min_price` /
`max_price`, `condition`, `seller_type` (`private` / `business`),
`olx_delivery` (not on kz or uz), `with_photos`, `region_id` / `city_id` /
`district_id` with `distance_km`, and the category's own `filter_*` keys
from `filters()`. A query with no exact match returns the closest ads. When
the site converts a price (olx.uz y.e. to UZS, EUR to RON on ro, USD / EUR
to UAH on ua), `price["value"]` is the converted figure and
`original_value` / `original_currency` keep what the seller entered. Jobs
carry `salary`. Private sellers' names, phone numbers, emails, exact map
positions, last-seen times and car VINs are never returned, and phone
numbers and emails in ad text are replaced; `business_name` is set for
business sellers only. OLX shows no seller ratings or reviews. Failed calls
are not charged; a not-found is a charged 404, and an ended ad answers the
same 404 as a missing one ("not found or no longer active"). No view
counts, phone numbers, messaging, delivery prices, checkout, average prices,
notifications or price history: to watch for new listings or track prices,
poll `sort="newest"` and store your own.

### 43. Grocery -- Kroger, QFC and Fred Meyer

Kroger grocery data, namespace `kroger`, 8 endpoints: `search`, `product`,
`prices`, `stores`, `category`, `deals`, `coupons`, `suggestions`. Every
method takes `banner`: `kroger` (kroger.com, default), `qfc` (QFC, qfc.com:
Washington and Oregon) or `fred_meyer` (Fred Meyer, fredmeyer.com: the
Pacific Northwest and Alaska, grocery plus general merchandise, apparel and
home). Other Kroger banners (Ralphs, King Soopers, Fry's, Harris Teeter,
Smith's...) are not supported yet. Prices are integer cents (`price` 399 =
$3.99) and differ by banner and by store. Every method raises the request
timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
kroger = client.kroger

# --- Search: prices are those of a store the site chooses (returned in store).
res = kroger.search("coffee", banner="qfc")["data"]
print(res["total"], res["count"], res["store"]["location_id"], res["store"]["name"])
for p in res["products"][:5]:
    print(p["upc"], p["name"], p["price"], p["promo_price"], p["price_display"])

# --- A specific store: find it, then price up to 25 UPCs there.
stores = kroger.stores(zip="97201", banner="fred_meyer")["data"]["stores"]
store_id = stores[0]["location_id"]
prices = kroger.prices(store_id, ["0001111050438"])["data"]
for item in prices["items"]:
    print(item["upc"], item["price"], item["promo_price"], item["in_stock"],
          item["stock_level"], item["quantity"], item["aisle"])
print(prices["not_found"])

# --- Product detail, a category listing and this week's digital deals.
milk = kroger.product(upc="0001111050438", banner="fred_meyer")["data"]
print(milk["name"], milk["price"], milk["rating"], milk["store_location"])
beer = kroger.category(taxonomy_id="08190", slug="Import-Beer", banner="qfc")["data"]
deals = kroger.deals(banner="qfc")["data"]
print(beer["category"], beer["total"], deals["deals_week"], deals["total"])

# --- Digital coupons at one store (listed, never clipped) and suggestions.
c = kroger.coupons(store_id="70100011", category="Dairy")["data"]
print(c["total_at_store"], c["has_more"], [x["title"] for x in c["coupons"][:3]])
print(kroger.suggestions("almond mi", banner="qfc")["data"]["suggestions"])
```

`search`, `product`, `category` and `deals` return the prices, promotions,
stock and aisle of a store the site chooses for the request (`store`: it can
change between calls and cannot be picked). For one store's price, stock and
aisle, take a `location_id` from `stores()` and pass it as `store_id` to
`prices()`; QFC store ids start with 705, Fred Meyer ids with 701. `search`,
`category` and `deals` serve the first page only (up to 24 products) and
cannot be sorted: `page` above 1 is a 400 and is not charged. `in_stock` is
None when the store has no stock record for the item. Ratings are average,
count and star distribution; review text is not available. `stores()` takes
exactly one of `zip`, `query` or `store_id` and returns fuel center
locations, not fuel prices. `coupons()` pages 24 at a time (`has_more`) and
only lists coupons: no account is used and nothing is clipped. `deals()` is
the weekly digital deals list; the printed weekly ad circular is not
available. 2 credits for `search` and `product`, 3 for `prices`, 1 for the
rest. Failed calls are not charged; an unknown UPC or store id is a charged
404.

### 44. Grocery -- Publix weekly ad, BOGO deals and store prices

Publix grocery data, namespace `publix`, 11 endpoints at 1 credit each:
`search`, `product`, `category`, `categories`, `weekly_ad`, `extra_savings`,
`coupons`, `savings_search`, `order_ahead`, `stores`, `suggestions`. Every
price endpoint is store-scoped: pass `store_id`, a Publix store number from
`stores()` (str or int). Prices and promotions differ by store. Every method
raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
publix = client.publix

# --- Find a store: store_id feeds every other method.
stores = publix.stores(zip="33101", limit=5)["data"]["stores"]
store_id = stores[0]["store_id"]
print(store_id, stores[0]["name"], stores[0]["weekly_ad_break_day"])

# --- This week's ad at that store: BOGO, sale prices, multi-buys.
ad = publix.weekly_ad(store_id, bogo_only=True)["data"]
print(ad["ad"]["start_date"], ad["ad"]["end_date"], ad["count"])
for item in ad["items"][:5]:
    print(item["title"], item["savings_text"], item["deal_type"], item["price"])

# --- Search: price is a number only when Publix shows one (promo or order-ahead).
res = publix.search("chicken", store_id, on_sale=True, sort="savings_amount")["data"]
for p in res["items"][:5]:
    print(p["item_code"], p["title"], p["aisle"], p["price"], p["price_text"], p["promo"])

# --- Pub Subs and the deli / bakery order-ahead menu, with this store's prices.
subs = publix.order_ahead(store_id)["data"]
print([(s["title"], s["price"]) for s in subs["items"][:3]])

# --- Product card plus nutrition facts by Publix item code (not UPC).
sub = publix.product("90355", store_id)["data"]
print(sub["title"], sub["price"], sub["nutrition"][0]["serving_size"])

# --- Extra Savings, digital coupons (listed, never clipped), or one keyword across all.
extra = publix.extra_savings(store_id)["data"]
print(extra["period"], extra["count"])
coupons = publix.coupons(store_id)["data"]
print([(c["title"], c["value"], c["valid_to"]) for c in coupons["items"][:3]])
hits = publix.savings_search("coffee", store_id)["data"]
print([(h["saving_type"], h["title"]) for h in hits["items"][:5]])
```

Publix does not show regular shelf prices online: `price` is a number only
for items on promotion (weekly ad, BOGO, multi-buy, Extra Savings) and for
order-ahead items, and None otherwise; it is never estimated. Multi-buys
("2 for $5.00") carry `bundle` {quantity, price}. A Publix Chicken Tender Sub
was measured at $12.09 in Miami (store 1614) and $11.99 in Atlanta (store
1825). Weekly ads run Thursday to Wednesday in Florida and Wednesday to
Tuesday in Georgia and North Carolina (`weekly_ad_break_day` per store);
English ad only. `search` and `category` serve 48 items per page,
`order_ahead` 60. Products are keyed by Publix item code: Publix does not
publish UPCs, ingredients, allergens or reviews online. `category()` takes
`category_url` or `category_id` (from `categories()`); `stores()` takes `zip`,
`city` with `state`, or `store_id`. No cart or ordering. Failed calls are not
charged; an unknown item code or store id is a charged 404.

### 45. Retail -- IKEA prices by country, stock by store and product data

IKEA product data across 55 markets, namespace `ikea`, 12 endpoints at 1
credit each: `search`, `product`, `reviews`, `category`, `categories`,
`deals`, `suggestions`, `stores`, `stock`, `items`, `compare`, `as_is`.
`compare` costs 1 credit per market that answered. `country` is the market
code (default `us`); `language` one of that market's languages (ca en/fr, be
nl/fr/en, ch de/fr/it/en, us en/es ...). `product` and `reviews` raise the
request timeout to at least 180s, the rest to 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
ikea = client.ikea

# --- IKEA prices by country: one article number on up to 10 markets, each in its own currency.
cmp = ikea.compare("80275887", ["de", "fr", "se", "nl", "es", "it"])["data"]
for m in cmp["markets"]:
    print(m["country"], m["found"], m["currency"], m["price"], m["previous_price"], m["price_tag"])

# --- Search one market, in one of its languages, sorted and filtered.
res = ikea.search("kallax", country="de", sort="price_asc", page_size=48)["data"]
print(res["total"], res["currency"])
for p in res["items"][:5]:
    print(p["item_no"], p["name"], p["type_name"], p["price"], p["price_tag"], p["rating_count"])

# --- Full product: measurements, materials, packaging, assembly PDFs, variants.
prod = ikea.product(item_no="20522046")["data"]
print(prod["name"], prod["type_name"], prod["price"], prod["currency"])
print(prod["packaging"]["number_of_packages"], [v["type"] for v in prod["variants"]])

# --- Stores, then stock level (not a quantity) at one store for up to 100 items.
stores = ikea.stores(country="us", query="Burbank")["data"]["stores"]
stock = ikea.stock(["20522046", "20631663"], stores[0]["store_id"])["data"]
print([(i["item_no"], i["store_availability"]["status"]) for i in stock["items"]])

# --- Deal lists, the 20 newest reviews, and one store's As-is (second-hand) offers.
deals = ikea.deals("new_lower_price", country="gb")["data"]
print(deals["total"], [(d["name"], d["price"], d["previous_price"]) for d in deals["items"][:3]])
reviews = ikea.reviews(item_no="80275887", country="de")["data"]
print(reviews["rating"], reviews["rating_count"], len(reviews["reviews"]))
asis = ikea.as_is("257")["data"]
print(asis["total"], [(o["title"], o["min_price"], o["original_price"]) for o in asis["offers"][:3]])
```

Markets: `search` and `product` cover 55, the 50 ikea.com markets (us ca gb
ie de at ch fr be nl dk se no fi ee lv lt pl cz sk hu hr si rs ro pt es it il
ae sa kw qa bh om jo eg ma in my sg ph th jp kr au nz mx cl co) plus cn
(ikea.cn), pr (Puerto Rico), do (Dominican Republic), es_islands (Canary and
Balearic islands, with `island`) and is (Iceland). `category`, `deals`,
`suggestions` and `items` serve the 50 ikea.com markets plus cn; `reviews`,
`categories`, `stores`, `stock` and `compare` the 50 ikea.com markets; `as_is`
us, gb, de, fr, se, jp, nl, es, it, pl, au, ch and at. Ukraine, Greece,
Cyprus, Bulgaria, Hong Kong, Taiwan, Indonesia and Turkey are not available.
Data comes in the market's language and prices in its own currency, never
converted: on 2026-11-13 KALLAX 80275887 was EUR 49.99 in de and nl, EUR
59.99 in fr and SEK 599 in se. Some markets (us, ca, jp, au, kr, in, my, sg,
ph ...) sell the same product under a different article number, so `found`
is False there. `reviews` returns the 20 most recent reviews the product page
shows (no paging, sort or star filter). Ratings are what each market's site
shows: many markets share one pool (KALLAX: 8,241 in Germany, Spain, Sweden),
others have their own (France 2,760, Italy 1,887) and some show none (Estonia,
Latvia, Lithuania, Israel, Iceland). `stock` is a level per store (in_stock_high, in_stock_low, out_of_stock), not
a quantity. A product call can take up to about 100 seconds. Puerto Rico,
Dominican Republic and the islands return the first 40 search results only,
and franchise products (pr, do, es_islands, is) return basic detail. Pass
article numbers as str to keep leading zeros. Failed calls are not charged;
an unknown article number, category or store id is a charged 404.

### 46. Retail -- Wayfair prices, sale and was price, reviews and delivery

Wayfair product data for wayfair.com, wayfair.ca (English or French),
wayfair.co.uk and wayfair.ie, plus Wayfair's US sites AllModern, Birch Lane,
Joss & Main and Perigold. Namespace `wayfair`, 4 endpoints at 1 credit each:
`search`, `product`, `category`, `deals`. `country` is the market (`us`
default, `ca`, `gb`, `ie`), `language` is `en` or `fr` on `ca`, and `site`
picks a US banner site (`search`, `product`, `category`). The request timeout
is raised to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
wayfair = client.wayfair

# --- Search: sort by price or rating, filter by sale, closeout, open box, brand id, rating.
res = wayfair.search("office chair", sort="price_asc", on_sale=True)["data"]
print(res["total"], res["total_is_approximate"], res["currency"], res["redirected_to"])
for p in res["items"][:5]:
    print(p["sku"], p["name"], p["price"], p["was_price"], p["price_label"], p["badge"])

# --- One product: price, sale price, was price, badge, stock, options, 5 reviews,
# and the delivery estimate for a ZIP (us and ca only).
prod = wayfair.product(sku="W005006988", zip="10001")["data"]
print(prod["price"], prod["sale_price"], prod["was_price"], prod["percent_off"], prod["badge"])
print(prod["rating"], prod["review_count"], prod["rating_histogram"], len(prod["reviews"]))
print([(d["name"], d["date_min"], d["text"]) for d in prod["delivery"]])

# --- Option choices carry no price: one call per option_id for its price and stock.
for choice in prod["options"][0]["choices"][:3]:
    opt = wayfair.product(sku="W005006988", option_id=choice["option_id"])["data"]
    print(choice["name"], opt["price"], opt["was_price"], opt["stock_status"])

# --- A category's grid (48 per page), another market, and the current sale events.
cat = wayfair.category(category_id="413892", sort="rating")["data"]
print(cat["category"]["name"], cat["total"], len(cat["items"]))
uk = wayfair.search("sofa", country="gb")["data"]
print(uk["currency"], [(i["name"], i["price"]) for i in uk["items"][:3]])
events = wayfair.deals()["data"]
print(events["count"], [e["title"] for e in events["events"][:5]])
```

Prices are numbers in the market's currency (USD, CAD, GBP, EUR), never
converted. `was_price` is Wayfair's strikethrough price: Wayfair's terms state
it is the manufacturer's suggested price or the highest price Wayfair offered
or sold the item at in the past, and its Sale label means a discount against a
price in the previous 90 days. Wayfair shows no price history, so poll
`price`, `sale_price`, `was_price` and `badge` on a schedule to build one.
`product` returns the 5 reviews the page shows plus the rating histogram and
review summary (no review paging). Keyword pages return 30 results (category
pages 48) and `total` is approximate. `brand` takes brand ids
(`items[].brand.id`), not names. `zip` delivery estimates are us and ca only.
`deals` lists sale events (event id, title, URL, image) without expanding
them: use `on_sale`, `closeout` or `open_box` on `search` or `category` for
products. Wayfair no longer sells in Germany or Austria. Failed calls are not
charged; an unknown SKU or category is a charged 404.

### 47. Retail -- Ashley Furniture prices, Regular Price, reviews, deals and stores

Ashley Furniture product data for ashleyfurniture.com, plus search and product
on Ashley's licensed storefronts in Canada, Mexico, the Philippines, Saudi
Arabia and Turkey. Namespace `ashley`, 6 endpoints: `search`, `product`,
`category`, `deals`, `stores`, `store`. `search` and `product` cost 2 credits
on `us` (the default) and `mx` and 1 credit on `ca`, `ph`, `sa` and `tr`;
`category`, `deals`, `stores` and `store` are us only at 2 credits. The
request timeout is raised to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
ashley = client.ashley

# --- Search (us): 48 per page, exact total, sort by price, newest, rating or name.
res = ashley.search("sofa", sort="price_asc")["data"]
print(res["total"], res["priced_for"])  # {'zipcode': ..., 'price_zone': ...}
for p in res["items"][:5]:
    print(p["sku"], p["name"], p["price"], p["regular_price"], p["discount_percent"])

# --- One product: price vs Regular Price, badges, stock, the first 10 reviews and Q&A.
prod = ashley.product(sku="5950418")["data"]
print(prod["price"], prod["regular_price"], prod["priced_for"], prod["stock"]["status"])
print(prod["rating"], prod["review_count"], prod["rating_histogram"], len(prod["reviews"]))

# --- A category grid (30 per page) with facet filters, and a deal event.
cat = ashley.category(path="furniture/living-room/sofas", filters={"facetUpholsteryDesign": "Chaise"})["data"]
print(cat["category"]["name"], cat["total"], [f["id"] for f in cat["facets"]])
deals = ashley.deals(event="black_friday", sort="price_desc")["data"]
print(deals["event_name"], deals["total"])

# --- Stores near a point (coordinates only), then one store's address and hours.
near = ashley.stores(40.7506, -73.9972, radius=25)["data"]
store = ashley.store(store_id=near["stores"][0]["store_id"])["data"]
print(store["name"], store["phone"], store["address"], store["hours"][0])

# --- A licensed storefront: search, then product by handle (not sku).
mx = ashley.search("sofa", country="mx")["data"]
item = ashley.product(handle=mx["items"][0]["handle"], country="mx")["data"]
print(mx["currency"], item["name"], item["price"], item["regular_price"])
```

Prices are numbers in the market's currency (USD, CAD, MXN, PHP, SAR, TRY),
never converted. `regular_price` is Ashley's own Regular Price, which Ashley's
terms define as its highest advertised price in store and online, offered to
customers using special long-term financing. Ashley prices vary by region and
there is no ZIP input: every us answer returns `priced_for` (`zipcode`,
`price_zone`), the ZIP and price zone Ashley priced that answer for, so two
calls can come back priced for different zones and consecutive pages can
overlap slightly. `product` returns the first 10 reviews the page shows plus
the rating histogram, customer photos and Q&A (no review paging). Search facets
are informational: filter with `category`. On the licensed storefronts
`search` returns up to 10 matches (`tr` its first results page) with no paging
or sort, and `product` takes `handle` or `url`, not `sku`. `deals` events are
`black_friday`, `clearance` and `hot_buys`. `stores` takes coordinates only (no
ZIP or city lookup) and lists stores alphabetically; call `store` for the
address, phone and hours. Failed calls are not charged; an unknown item number,
category or store is a charged 404.

### 48. Retail -- Maisons du Monde promo prices, reviews, store stock and marketplace sellers

Maisons du Monde (furniture and home decor) for France, Belgium (French or
Dutch), Luxembourg, the Netherlands, Germany, Spain, Italy, Portugal and
Switzerland (French, German or Italian). Namespace `maisonsdumonde`, 9
endpoints, 1 credit each: `search`, `product`, `category`, `deals`, `reviews`,
`stores`, `store`, `availability`, `seller`. Pick the market with `country`
(default `fr`) and, on Belgium and Switzerland, the language with `language`.
The request timeout is raised to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
mdm = client.maisonsdumonde

# --- Search: 40 per page with the exact total; price next to the crossed-out price.
res = mdm.search("table")["data"]
print(res["total"], res["currency"])
for p in res["items"][:5]:
    print(p["id"], p["name"], p["price"], p["was_price"], p["discount_percent"], p["sold_by"])

# --- The same product on another storefront: Switzerland is priced in CHF.
fr = mdm.product(id="204172")["data"]
ch = mdm.product(id="204172", country="ch", language="de")["data"]
print(fr["price"], fr["was_price"], fr["currency"], ch["price"], ch["was_price"], ch["currency"])
print([m["country"] + "/" + m["language"] for m in fr["markets"]])

# --- Black Friday, or one category's discounted items at 30% off or more.
bf = mdm.deals(country="de")["data"]
cat = mdm.deals(category="canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f", min_discount=30)["data"]
print(bf["event"]["name"], bf["total"], cat["total"])

# --- Reviews: pooled across markets, translated into the request language.
rev = mdm.reviews("186339", sort="rating_asc")["data"]
print(rev["rating"], rev["rating_histogram"], rev["reviews"][0]["source_market"])
more = mdm.reviews("186339", sort="rating_asc", cursor=rev["next_cursor"])["data"]

# --- Stores near a postcode, then one item's stock at a store and the delivery from-price.
near = mdm.stores("75011")["data"]
stock = mdm.availability("204172", near["stores"][0]["id"])["data"]
print(stock["in_stock"], stock["quantity"], [(d["type"], d["from_price"]) for d in stock["delivery"]])

# --- A marketplace seller (fr, de, es, it) and only items sold by Maisons du Monde.
seller = mdm.seller(seller_id="2066")["data"]
print(seller["seller"]["name"], seller["seller"]["rating"], seller["total"])
own = mdm.search("chaise", sold_by="mdm", on_sale=True)["data"]
```

Prices are numbers in the market's currency, never converted, and can differ
by market: measured on 2026-11-14 on about 170 discounted sofas, Luxembourg,
the Netherlands, Germany, Spain, Italy and Portugal matched France on every
item, Belgium differed on 19, and Switzerland is priced separately in CHF
(round mirror 204172: 74.99, now 37.45 EUR on every euro market; 91.90, now
45.95 CHF). Read each market you report. `was_price` is the
crossed-out price shown next to a discount and `discount_percent` the page's
own percent off; `eco_participation` (fr) is the French furniture recycling
fee included in the price. Maisons du Monde shows no 30-day lowest price and no
price history, so poll to track changes. `search`, `product`, `category`,
`deals` and `reviews` serve all nine markets; `stores`, `store` and
`availability` serve fr, be, de, es, it, pt and ch (not nl or lu); `seller`
and the `seller` / `sold_by` filters serve the marketplace markets fr, de, es
and it. Search tiles carry `sold_by` but not the seller name (`product` has
it). The German site does not sort keyword results, so a sorted search on
`de` comes back in relevance order with a note. Reviews have no star filter
and no id, title or verified flag; a product with no reviews is a charged 404.
Home delivery is a from-price per product and market (no postcode-exact
cost). `availability` covers Maisons du Monde items only (marketplace items
are not stocked in stores). `deals` events are `black_friday` (every market
while it runs) and `second_chance` (fr: used and returned items). No search
suggestions. Failed calls are not charged; a not-found is charged.

### 49. Marketplace -- Trendyol seller prices, buy box, reviews, coupons and rankings

Trendyol (Turkey's largest online marketplace) and its international
storefronts across Europe, the Gulf and Azerbaijan: 35 markets. Namespace
`trendyol`, 12 endpoints, 1 credit each: `search`, `product`, `category`,
`brand`, `reviews`, `questions`, `seller`, `deals`, `coupons`, `rankings`,
`suggestions`, `delivery`. Pick the market with `country` (default `tr`) and
the language with `language` (default the market's first). The request
timeout is raised to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
ty = client.trendyol

# --- One product: the buy-box seller and every other seller's price and score.
p = ty.product(content_id=975557855)["data"]
bb = p["buy_box"]
print(p["name"], p["currency"], bb["seller"]["name"], bb["seller"]["score"], bb["price"])
for o in p["other_sellers"]:
    print(o["seller"]["name"], o["seller"]["score"], o["price"], o["original_price"], o["lowest_price_badge"])

# --- Search: 36 per page; sponsored cards are flagged and repeat across pages.
res = ty.search("telefon", sort="price_asc", lowest_price_days=30)["data"]
print(res["total"], res["total_capped"], res["count"], res["sponsored_count"])
organic = [i for i in res["items"] if not i["sponsored"]]

# --- An international storefront: its own price list and language.
ro = ty.search("rochie", country="ro", language="ro")["data"]
print(ro["currency"], ro["items"][0]["name"], ro["items"][0]["price"])

# --- Reviews (masked authors only) and answered seller questions.
rev = ty.reviews(content_id=975557855, sort="newest")["data"]
print(rev["rating"], rev["rating_histogram"], rev["reviews"][0]["author"])
qa = ty.questions(content_id=975557855)["data"]

# --- Coupons belong to each seller's listing (tr only); pass another seller's id.
cp = ty.coupons(content_id=1164743007)["data"]
print([(c["discount"], c["discount_type"], c["min_basket"], c["valid_until"]) for c in cp["coupons"]])

# --- Top-100 rankings, flash deals (tr only) and a delivery estimate for Istanbul / Sisli.
top = ty.rankings(56, ranking="best_seller")["data"]
flash = ty.deals(type="flash")["data"]
dl = ty.delivery(content_id=975557855, city_id=133, district_id=54)["data"]
print([(l["seller"], l["delivery"]) for l in dl["listings"][:3]])
```

Markets and languages: tr (TRY; tr, en or ar), de and at (EUR; de), fr, be,
hr, dk, ee, fi, it, lv, lt, nl, pt, si, es, se and lu (EUR; en), bg (EUR; bg
or en), gr (EUR; el or en), sk (EUR; sk or en), cz (CZK; cs or en), hu (HUF;
hu or en), pl (PLN; pl or en), ro (RON; ro or en), rs (RSD; sr or en), ua
(UAH; uk or en), md (MDL; ro or en), ae (AED; en or ar), sa (SAR; ar or en),
qa, kw, om and bh (QAR, KWD, OMR, BHD; ar or en) and az (AZN; tr). `deals`
and `coupons` are tr only; `rankings` is not on the 15 English-language EU
storefronts (fr, be, hr, dk, ee, fi, it, lv, lt, nl, pt, si, es, se, lu),
which have no ranking lists; `delivery`'s `city_id` / `district_id` are tr
only (Istanbul 133, Sisli 54; there is no city list). Every other endpoint
serves all 35. The international storefronts have their own price lists, not
a currency conversion of the Turkish price (measured on 2 products on
2026-11-15), and their items are sold by Trendyol itself or by other sellers
(check `buy_box` and `other_sellers`). Trendyol's developer
FAQ says the buy box is chosen by algorithm metrics, not price alone, so
compare `buy_box` with `other_sellers`. `lowest_price_badge` is the site's
"lowest price of the last N days" tag (7, 10, 14, 30 or 90 days): a day
count, not a numeric 30-day lowest price, and there is no price history, so
poll to track changes. Search lists at most 138 pages and `total` stops at
100,000 (`total_capped`); search cards give favourites and orders as the
site's rounded text. Reviews carry the site's masked author only and no
seller e-mail, tax number or address is returned. Failed calls are not
charged; a not-found is charged.

### 50. Games -- Nintendo eShop regional prices, sales, deals, releases and DLC

The Nintendo eShop and My Nintendo Store in 46 countries. Namespace
`nintendo`, 6 endpoints, 1 credit each: `search`, `product`, `prices`,
`deals`, `releases`, `dlc`. Pick the market with `country` (default `us`) and
the language with `language` (default the market's first). The request
timeout is raised to at least 120s (Americas searches take about 8 to 13s).

```python
from scavio import ScavioClient

client = ScavioClient()
nd = client.nintendo

# --- One game's price, sale price and sale end in each eShop country of its region.
# Item ids (nsuid) are per eShop region: look the game up in the region first.
p = nd.product(nsuid="70010000095431")["data"]["product"]  # an Americas id
for cc in ("us", "ca", "mx", "br", "ar", "cl", "co", "pe"):
    row = nd.prices([p["nsuid"]], country=cc)["data"]["prices"][0]
    print(cc, row["currency"], row["price"], row["regular_price"], row["sale_price"], row["sale_end"])

# --- A European id priced in Poland and Sweden (the English catalog, local prices).
for cc in ("pl", "se"):
    d = nd.prices(["70010000096802", "70010000063715"], country=cc)["data"]
    print(cc, d["currency"], [(r["nsuid"], r["price"]) for r in d["prices"]], d["not_found"])

# --- Search: Europe and Japan have an nsuid per item; Americas tiles carry a slug only.
gb = nd.search("mario", country="gb", sort="price_asc", platform="switch_2")["data"]
print(gb["total"], gb["total_pages"], [(i["nsuid"], i["title"], i["price"]) for i in gb["items"][:3]])
us = nd.search("mario")["data"]
first = nd.product(slug=us["items"][0]["slug"])["data"]["product"]

# --- Deals: Americas = Nintendo's featured sale pages; Europe / Japan = every game on sale.
deals = nd.deals(sort="ending_soon")["data"]
print([s["sale"] for s in deals["sales"]], [(i["title"], i["discount_percent"], i["sale_end"]) for i in deals["items"][:3]])

# --- New and upcoming releases, and a game's DLC with prices.
new = nd.releases(country="gb")["data"]
dlc = nd.dlc(slug="super-smash-bros-ultimate-switch")["data"]
print(dlc["game"]["title"], dlc["count"], [(x["title"], x["type"], x["price"]) for x in dlc["dlc"][:3]])
```

Markets and languages: Americas us (USD), ca (CAD; en or fr), mx (MXN; es),
br (BRL; pt), ar (ARS), cl (CLP), co (COP) and pe (PEN) (es); Europe in the
market's language: gb (GBP) and ie (EUR) (en), de and at (EUR; de), ch (CHF;
de, fr or it), fr, be (fr or nl), nl, lu (fr), it, es and pt (EUR), au (AUD),
nz (NZD) and za (ZAR) (en); pl (PLN), cz (CZK), se (SEK), no (NOK), dk (DKK),
fi, sk, hu, ro, bg, gr, hr, si, ee, lv, lt, mt and cy (EUR) have no Nintendo
site of their own and read the English European catalog with that country's
own prices; jp (JPY; ja). `prices` also serves kr (KRW), hk (HKD), tw (TWD)
and il (EUR, European item ids). ph (no Philippines item ids published yet),
ru (no eShop), uk (use gb) and countries with no eShop data answer 400.

Item ids (`nsuid`) are per eShop region: Americas, Europe (EU / EFTA, GB, AU,
NZ, ZA, IL), Japan, Korea, and Hong Kong + Taiwan (Taiwan uses Hong Kong ids).
An id from one region is `not_found` in another and there is no cross-region
title mapping: look the game up with `search` or `product` in that region,
then call `prices` for any country of the region (up to 50 ids per call).
Prices are always the requested country's eShop price in its currency;
`sale_start` and `sale_end` are the eShop's own sale window. Nintendo shows
no price history or historical low: poll `prices` to build one. Americas
`deals` are Nintendo's featured sale pages, not every discounted game (check
any id with `prices`); Europe and Japan `deals` are every game on sale.
Americas `search` sorts by relevance or newest only and takes no filters, and
the Americas `releases` lists are one page; an unsupported sort or filter
answers 400, never silently dropped. No user reviews (Nintendo's stores have
none; age ratings only), no best-seller charts and no autocomplete. Failed
calls are not charged; a not-found is charged.

### 51. Fashion -- H&M prices by country, member prices, online stock by size and stores

H&M in 47 countries. Namespace `hm`, 9 endpoints: `search`, `product`,
`stock`, `stores`, `category`, `deals`, `new_arrivals`, `suggestions`,
`production`. `product` costs 2 credits, every other endpoint 1. Pick the
market with `country` (default `us`) and the language with `language`
(default the market's first). The request timeout is raised to at least 120s
(`product` can take up to about a minute).

```python
from scavio import ScavioClient

client = ScavioClient()
hm = client.hm

# --- One article's price in several markets: article codes are the same everywhere.
for cc in ("gb", "ca", "ch", "pl", "se"):
    p = hm.product(article_code="1347936009", country=cc)["data"]
    print(cc, p["currency"], p["price"], p["regular_price"], p["sale_price"], p["member_price"])

# --- Online stock by size (not store stock), for every colour of the product.
st = hm.stock(article_code="1310382004")["data"]
print(st["sizes_in_stock"], "/", st["sizes_total"])
for c in st["colors"]:
    print(c["article_code"], c["name"], [(s["label"], s["in_stock"], s["few_left"]) for s in c["sizes"]])

# --- Search, a category grid (category ids are the same in every market) and the sale grid.
res = hm.search("jeans", country="de", language="de", sort="price_asc")["data"]
print(res["total"], [(i["article_code"], i["title"], i["price"]) for i in res["items"][:3]])
dresses = hm.category("ladies_dresses", country="gb")["data"]
sale = hm.deals(country="gb", department="men")["data"]  # may be empty between sales
print(sale["total"], [(i["title"], i["sale_price"], i["discount_percent"]) for i in sale["items"][:3]])

# --- Stores in a city, then that store's assortment.
store = hm.stores(city="New York")["data"]["stores"][0]
print(store["store_code"], store["name"], store["opening_hours"][0])
in_store = hm.search("jeans", store=store["store_code"])["data"]

# --- New arrivals, suggestions and where an article is made.
new = hm.new_arrivals(country="se", language="sv")["data"]
print([s["text"] for s in hm.suggestions("hoodie")["data"]["suggestions"]])
made = hm.production(article_code="1310382004")["data"]
print(made["production_countries"], [s["name"] for c in made["countries"] for s in c["suppliers"]])
```

Markets and languages: us (USD), ca (CAD; en or fr), mx (MXN; es), gb (GBP),
ie (EUR), de and at (EUR; de), ch (CHF; de, fr or it), fr, be (nl or fr), nl,
it, es, pt (EUR), se (SEK), fi (EUR; fi or sv), dk (DKK), no (NOK), pl (PLN),
cz (CZK), sk (EUR), hu (HUF), ro (RON), bg (EUR), gr (EUR), rs (RSD), tr
(TRY), ua (UAH), il (ILS; he), hk and mo (HKD; zh or en), tw (TWD; zh or en),
jp (JPY), kr (KRW), in (INR), my (MYR), ph (PHP), sg (SGD), vn (VND), au
(AUD), each in its own language; and hr, cy, ee, lv, lt, lu and si on H&M's
shared English EUR store (answers say store `eu`). Every endpoint serves all
47 except `product` (not mo, tw or the shared EU store countries: use
`search` or `stock` there) and `stores` (not mo: H&M lists no stores there).
Countries where H&M runs a separate site (ae, eg, id, th, br, cn) or has no
online store, ru, and uk (use gb) answer 400 before anything is charged.

Article codes are global: the same 10-digit code (7-digit product code +
3-digit colour) in every market, so one code compares a price across markets
with one call per `country`. `price` is what a non-member pays now;
`member_price` is H&M's member price as shown to signed-in members;
`prior_price` is the earlier price H&M shows next to an EU markdown; `product`
adds `price_disclosure` where H&M shows one. `stock` is online stock per
size: H&M publishes no per-size store stock (`search` with `store` lists a
store's assortment). `product` carries the rating and the latest reviews H&M
shows (up to 10, with fit feedback): there is no full review list. Category
ids are the same in every market, and a category returns everything H&M files
under that id, which can be more than the site's curated page. H&M runs sales
in seasons, so `deals` may return an empty grid between sales. No price
history (poll to track changes), no checkout or member-only cart prices, and
H&M's sibling brands (COS, Weekday, & Other Stories, Monki, ARKET) are not
covered. Failed calls are not charged; a not-found is charged.

### 52. Fashion -- Zara prices by country, stock by size online and in stores

Zara in 102 storefronts. Namespace `zara`, 12 endpoints: `search`,
`product`, `materials`, `stock`, `stores`, `store_stock`, `categories`,
`category`, `deals`, `new_arrivals`, `prices`, `suggestions`. Pick the
market with `country` (default `us`) and the language with `language`
(default Zara's own default for the market). The request timeout is raised
to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
zara = client.zara

# --- Zara prices by country: one reference in up to 10 markets per call, each in its own currency.
p = zara.prices("4591/381", countries=["us", "gb", "es", "de", "fr", "it", "jp", "kr", "mx", "pl"])["data"]
for m in p["markets"]:
    print(m["country"], m["currency"], m["price"], m["old_price"], m["title"])
print("not sold in:", p["not_sold"])

# --- Search, then the product page (product_id + seo_slug) and its online stock by size.
res = zara.search("blazer")["data"]
print(res["total"], [(i["display_reference"], i["title"], i["price"]) for i in res["items"][:3]])
item = res["items"][0]
prod = zara.product(product_id=item["product_id"], slug=item["seo_slug"])["data"]
for c in prod["colors"]:
    print(c["name"], c["price"], [(s["name"], s["availability"]) for s in c["sizes"]])
st = zara.stock("588478514")["data"]
print(st["sizes_in_stock"], "/", st["sizes_total"])

# --- Materials and origin, as the product page states them.
mat = zara.materials("588478514")["data"]
print(mat["composition"], mat["origin"])

# --- Stores near a point, then units per size in those stores (sales floor vs stockroom).
stores = zara.stores(40.7128, -74.006)["data"]["stores"]
ids = [s["store_id"] for s in stores[:8]]
units = zara.store_stock("553306790", store_ids=ids)["data"]
print(units["stores_with_stock"], units["stores_without_stock"])

# --- Category tree, one category, the SPECIAL PRICES list and new arrivals.
tree = zara.categories(section="woman")["data"]
dresses = zara.category("2420896", sort="price_asc")["data"]
deals = zara.deals(section="woman")["data"]  # empty (not an error) where a market has no special-prices list
new = zara.new_arrivals(country="gb", section="woman")["data"]
print(zara.suggestions("jea")["data"]["suggestions"])
```

Credits are what each request spent (`credits_used` in the response): 2 per
call for `search`, `materials`, `stock`, `stores`, `categories` and
`category`; `product` 2 (4 when opened by `reference` or when the slug is
another market's or language's, 6 for both); `store_stock` 2 with
`store_ids`, 4 with `lat` + `lng`; `deals` 4 (2 when the market has no
special-prices category); `new_arrivals` 4; `prices` 2 per market that
answered; `suggestions` 2 (4 when the English fallback runs). China (`cn`,
Zara's separate site) costs 1 credit per call instead of 2.

Markets: the 102 Zara storefronts with an online store of their own, each in
its own currency and Zara's own languages (205 market-languages; the first
listed is Zara's default), e.g. us (USD; en, es), ca (CAD; en, fr), mx, br,
gb (GBP; the United Kingdom), ie, de, at, fr, be, nl, lu, it, es (es, en, eu,
gl, ca), pt, ch (CHF; en, fr, de, it), se, dk, no, fi, pl, cz, sk, hu, ro, bg,
gr, hr, si, rs, tr, ua, il, ae, sa, kw, qa, bh, om, jo, lb, eg, ma, tn, dz, in,
jp (JPY; ja, en), kr (KRW; ko, en), cn (CNY; zh, en), hk, mo, tw (zh-Hant,
en), sg, my, ph, th, id, vn, kh, au, nz, za and the rest of Latin America and
Europe Zara sells online in; ic is the Canary Islands, xe Abu Dhabi, Al Ain
and Ras Al Khaimah, xk Kosovo. The full list with currencies and languages is
in the `country` docstring. Every endpoint serves all 102 except `stores` and
`store_stock` (not ao or iq: Zara lists no stores there), `new_arrivals` (not
dz) and `suggestions` (not ad, al, am, az, ba, dz, mk, mo, uz or xk).
Belarus, uk (use gb) and the countries Zara serves only from its worldwide
store answer 400 before anything is charged.

References are global on Zara's international site, so `prices` compares
one reference across markets in a single call. A colour's product id is
usually the same across markets but can differ, and China (`cn`) runs its
own ids, so match across markets with the reference.
Prices are numbers in the market's own currency, never converted;
`old_price` is set only on a markdown. Zara runs seasonal sales and lists
special prices between them: `deals` resolves each market's special-prices
list live and answers an empty list (not an error) where a market has none
for the section; in fr, be, lu, mc and iq Zara lists special prices without a
previous price. `stock` is online stock per size; `store_stock` is units in
physical stores. `materials` gives composition, care and the country of
production as Zara states it (France shows traceability steps; no factory
names). Category ids are shared across the northern-hemisphere catalogue;
au, za and br run their own (get them from `categories`). No reviews (Zara
shows none), no price history (poll `prices`), and Inditex's other brands
(Pull&Bear, Massimo Dutti, Bershka, Stradivarius, Oysho, Zara Home, Lefties)
are not covered. Failed calls are not charged; a not-found is charged.

### 53. Fashion -- ASOS prices by country and currency, stock by size, reviews

ASOS in 235 countries. Namespace `asos`, 11 endpoints: `search`, `product`,
`stock`, `reviews`, `suggestions`, `category`, `categories`, `brands`,
`deals`, `new_arrivals`, `markets`. Pick the country with `country` (default
`gb`) and the currency with `currency` (default ASOS's own default for the
country). 1 credit per call. The request timeout is raised to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
asos = client.asos

# --- One product's price and online stock by size in several stores and currencies.
# Product ids are the same on every store. Countries on the same store + currency share one
# price list, except Ireland (its own euro prices on ASOS's European store).
for country, currency in [("gb", None), ("us", None), ("fr", None), ("au", None), ("ae", "AED")]:
    p = asos.product(product_id="210309625", country=country, currency=currency)["data"]
    print(p["store"], p["currency"], p["price"], p["previous_price"], p["rrp"], p["is_marked_down"])
    print([(v["size"], v["in_stock"], v["low_stock"]) for v in p["variants"]])

# --- Price and online stock of up to 100 ids in one call (variant ids; product() has the sizes).
st = asos.stock(["205338218", "206956133", "209793673"], country="de")["data"]
for prod in st["products"]:
    print(prod["product_id"], prod["price"], [(v["variant_id"], v["in_stock"]) for v in prod["variants"]])
print("not sold here:", st["not_found"])

# --- Search (at most 2,088 results reachable: max_reachable), then filter with facet ids.
res = asos.search("jeans", sort="price_asc", gender="women", range="petite")["data"]
print(res["total"], res["max_reachable"], [(i["product_id"], i["title"], i["price"]) for i in res["items"][:3]])

# --- Reviews: gb, us, au, europe and international share one English pool; es, it, nl, se,
# dk and pl add own-language reviews; fr and de show only French or German. ASOS's labelled
# AI summary; no reviewer names.
rv = asos.reviews("210309625", sort="newest", page_size=50)["data"]
print(rv["summary"]["average"], rv["summary"]["count"], rv["ai_summary"])

# --- Brands: brand_id is a category id, so pass it to category().
brands = asos.brands(gender="women")["data"]["brands"]
brand_page = asos.category(str(brands[0]["brand_id"]), sort="newest")["data"]

# --- Navigation, the SALE and NEW IN lists, suggestions and the markets table.
tree = asos.categories(country="it")["data"]
sale = asos.deals(country="us", gender="men")["data"]
new = asos.new_arrivals(country="au")["data"]
print(asos.suggestions("dre", country="de")["data"]["suggestions"])
mk = asos.markets(country="il")["data"]
print(mk["selected"]["currencies"], mk["count"])
```

Markets: the 235 countries in ASOS's own country selector, served by 13 ASOS
stores. Eleven have a site of their own in their own language: gb (GBP), us
and pr (USD), fr and mc (EUR, French; the French overseas territories in USD),
de and at (EUR, German), es and ad (EUR, Spanish), it, sm and va (EUR,
Italian), au (AUD), dk (DKK), nl (EUR), pl (PLN) and se (SEK). ASOS's European
store (33 countries, English: ie, pt, be, fi, gr, cz, hu, ro, no ...) and its
international store (170 countries, English: ca, mx, in, za, ch, nz, ae, sa,
hk, il, jp, kr, sg, tw, cn ...) serve the rest. `currency` takes any currency
ASOS offers the country (245 country-currency combinations, e.g. ae AED or
GBP, il ILS, GBP or USD, jp USD or GBP); `markets` lists them. Every endpoint
serves every combination except `suggestions` on pl (ASOS's Polish store
answers no suggestions). Russia and Belarus (ASOS is not selling there), uk
(use gb) and countries ASOS does not list answer 400 before anything is
charged.

Product and category ids are the same on every store (titles come back in the
store's language). Countries served by the same ASOS store in the same
currency share one price list, except Ireland, which has its own euro prices on
ASOS's European store (measured 2026-11-16 on all 245 country-currency
combinations); which products are offered still differs by country. `price` is
the lowest size price when ASOS prices sizes differently (variants carry each
size's price). Prices are numbers in
the requested currency, never converted: `price`, `previous_price` (ASOS's
"was"), `rrp`, `lowest_price_30d` where ASOS shows it, `is_marked_down`,
`is_outlet`, `discount_percent` and `discount_basis` (`previous_price` or
`rrp`). `stock` is online stock per variant (ASOS has no physical stores) and
carries variant ids, not size names: `product` carries the sizes. Which reviews
come back depends on the store: gb, us, au and ASOS's European and
international stores share one English review pool; es, it, nl, se, dk and pl
add reviews written in their own language to that pool; fr and de show only
reviews written in French or German (each review carries its language). Up to
50 per page, sorted by relevance, newest, oldest or rating, filtered by star
rating; syndicated reviews are labelled. Keyword search serves at most 2,088
results whatever `total` says (`max_reachable`); category, `deals` and
`new_arrivals` lists page through everything. The `search` brand filter takes
brand facet ids from a search answer; `brands` returns category ids to pass to
`category`. `deals` is ASOS's sale category per gender, `new_arrivals` its new-in
category. No outlet (ASOS's outlet categories are empty), no promo codes
(shown only to signed-in shoppers) and no price history (poll `stock`). Failed
calls are not charged; a not-found is charged.

### 54. Marketplace -- Mercari sold prices, listings, items and sellers, US and Japan

Mercari US (mercari.com, USD, English) and Mercari Japan (jp.mercari.com, JPY,
Japanese). Namespace `mercari`, 11 endpoints: `search`, `item`, `category`,
`categories`, `brands`, `brand`, `deals`, `trending`, `seller`,
`seller_reviews`, `shop`. Pick the market with `country` (`us`, the default,
or `jp`). 1 credit per call. The request timeout is raised to at least 240s
(Mercari Japan calls are slower than US: typically 10-20s, up to about a minute).

```python
from scavio import ScavioClient

client = ScavioClient()
mercari = client.mercari

# --- Asking prices vs sold prices for the same query, from one endpoint.
# status="sold" returns sold listings (sold and in transit) with their prices. On us,
# sold results come most recently sold first and match the keyword loosely: check titles.
on_sale = mercari.search("nintendo switch")["data"]
sold = mercari.search("nintendo switch", status="sold", sort="recently_sold")["data"]
print(on_sale["total"], [(i["title"], i["price"]) for i in on_sale["items"][:3]])
print(sold["total"], [(i["title"], i["price"], i["status"]) for i in sold["items"][:3]])

# --- One listing: price, the seller's earlier price, sold_at, shipping, likes, seller summary.
# Grids carry no likes and no sold time; item() has both. Sold items keep full data;
# sold_at is set when Mercari shows it (some sold items carry none).
it = mercari.item("m38943035688")["data"]
print(it["price"], it["original_price"], it["discount_percent"], it["status"], it["sold_at"])
print(it["shipping"], it["likes"], it["seller"])

# --- Mercari Japan: Japanese as sellers wrote it, prices in yen; comments on the item.
jp = mercari.search("ポケモンカード", country="jp")["data"]
jp_item = mercari.item("m65962821601", country="jp")["data"]
print(jp["page_size"], jp["max_page"], [c["text"] for c in jp_item["comments"][:3]])

# --- Categories, brands and their listings (ids are per market).
electronics = mercari.categories(parent_id="7")["data"]["categories"]
in_cat = mercari.category("797", status="sold")["data"]
nike = mercari.brands(query="nike")["data"]["brands"]
nintendo = mercari.brand("4591", sort="price_asc")["data"]

# --- US only: the deals filter (price dropped) and Mercari's trending keywords and brands.
deals = mercari.deals()["data"]
trending = mercari.trending()["data"]
print([(k["keyword"], k["rank_change"]) for k in trending["keywords"][:5]])

# --- Japan only: seller profile with good / normal / bad ratings, reviews, Mercari Shops shop.
seller = mercari.seller("477123966")["data"]
reviews = mercari.seller_reviews("477123966")["data"]
shop = mercari.shop("LThudSk3aoGvKcW6R3sA6m")["data"]
print(seller["seller"]["ratings"], reviews["summary"], shop["shop"]["name"])
```

Markets per endpoint: `search`, `item`, `category`, `categories`, `brands` and
`brand` on us and jp; `deals` and `trending` us only; `seller`,
`seller_reviews` and `shop` jp only. A market an endpoint does not serve,
Mercari UK (closed: `gb` / `uk`) and any other value answer 400 before
anything is charged. Item, category, brand and seller ids are per market: an
id from us is not valid on jp.

`status` is `on_sale` (default), `sold` (sold and in transit) or `all`, so
asking and sold prices for the same query come from one call each. On us,
Mercari orders sold results most recently sold first whatever relevance asks
(price sorts apply) and matches the keyword more loosely than on-sale results,
so check titles before comparing prices. Search depth: us 50 per page up to
page 20 (later pages can repeat earlier items: dedupe by `item_id`), jp 120
per page up to page 91; `total` stops at 10,000 on us and 15,000 on jp (that
many or more). On us, `free_shipping` is set only when you filter by
`shipping`; `item()` has `shipping.payer`. Sorts: relevance, newest, price_asc, price_desc, plus `likes` on jp
and `recently_sold` on us; jp `newest` follows Mercari Japan's own order,
where relisted items move up. Prices are numbers, US dollars on us and whole
yen on jp; `original_price` is the seller's earlier price when above `price`,
with `discount_percent` against it (never set on jp results). `brands` covers about 28,800 US and 52,600
Japanese brands in pages of 1,000; `categories` answers one level at a time on
us and the full tree (or one parent's children) on jp. `seller_reviews`
returns the most recent 100 reviews with no reviewer names; `shop` is the
Mercari Shops shop profile only (for its products use `search` with
`shops_only=True` or `item`). Not available: US seller profiles and reviews,
US search suggestions, Japanese trending and price-drop history. Failed calls
are not charged; a not-found is charged.

### 55. Marketplace -- bol.com competitor prices, lowest-priced seller offers, sellers and deals

bol.com, the Netherlands and Belgium (EUR). Namespace `bolcom`, 9 endpoints:
`search`, `product`, `offers`, `seller`, `seller_products`, `category`,
`brand`, `deals`, `campaign`. 2 credits per call; `product(ean=...)` is 4
(a search plus the product page, billed on what it actually cost). Pick the
storefront with `country` and `language`: nl-nl (`country="nl"`, the
default, Dutch), be-nl (`country="be"`, Dutch) or be-fr (`country="be"`,
`language="fr"`, French). The request timeout is raised to at least 240s.

```python
from scavio import ScavioClient

client = ScavioClient()
bolcom = client.bolcom

# --- Competitor prices on one product: the buy box, cheapest / fastest, offer counts.
# product_id is a 16-digit STRING: never pass it as an int.
p = bolcom.product("9300000239314960")["data"]
bb = p["buy_box"]
print(p["ean"], bb["price"], bb["reference_price"], bb["reference_price_type"], bb["seller"]["name"])
print(p["offer_count"], p["cheapest_new"], p["fastest_new"])

# --- The 10 lowest-priced offers on that product (price, condition, shipping cost, seller rating),
# with counts by condition for all its offers; has_more when bol has more (no paging).
# The list does not mark the buy box: compare offer_id with buy_box["offer_id"].
offers = bolcom.offers("9300000240171936")["data"]
print(offers["counts"], offers["has_more"], [(o["seller"]["name"], o["price"], o["condition"]) for o in offers["offers"]])

# --- By EAN (4 credits), on the French-language Belgian storefront.
by_ean = bolcom.product(ean="4242005483976", country="be", language="fr")["data"]
print(by_ean["requested_ean"], by_ean["product_id"], by_ean["storefront"])

# --- Search: up to page 10, filters, sponsored items flagged; list items carry no EAN.
res = bolcom.search("airpods", sort="price_asc", condition="new", delivery="tomorrow")["data"]
print(res["total"], res["max_page"], [(i["title"], i["offer"]["price"], i["sponsored"]) for i in res["items"][:5]])

# --- Sellers: rating out of 10, up to four sub-ratings, public trader data; and what they sell.
seller = bolcom.seller("1770745")["data"]["seller"]
print(seller["rating"], seller["rating_details"], seller["positive_percent"], seller["business"])
catalog = bolcom.seller_products("1767374", country="be")["data"]

# --- Category, brand (brand_id, not the brand_facet_id search filter), deals, promotions.
cat = bolcom.category("8440", sort="price_asc", deals_only=True)["data"]
apple = bolcom.brand("5070005")["data"]
deals = bolcom.deals()["data"]
promo = bolcom.campaign(deals["day_deal"]["campaign_id"])["data"]
```

Every endpoint serves all three storefronts. Product, EAN, category, seller
and offer ids are the same on every storefront; prices, offers and stock can
differ between the Netherlands and Belgium. On be-fr bol's own texts are
French, some partner titles and the review topics stay Dutch, and review texts
are bol's translation (`is_translated`). `reference_price_type` is `rrp` (the supplier's
recommended price) or `most_shown_price` (bol's most-shown non-promotional
price over the last 90 days); `discount_percent` is against it.
`brand_facet_id` (the `search` / `category` filter, a value id from the brand
facet: Apple 4294862300) and `brand_id` (items' `brand.brand_id`, `brand()`:
Apple 5070005) are different id spaces. Search stops at page 10 (about 280
results) and sorts by relevance (default), popularity, price_asc, price_desc,
rating or wishlist, with no newest sort; sorting by anything but relevance can
narrow bol's result set, and price sorts follow bol's own ordering (small
inversions against the live buy-box price occur). `seller_products`,
`category`, `brand` and `campaign` default to popularity, page 1 to 500, and do
not offer relevance; a campaign item's offer is its buy box, which does not
always carry the campaign's label. `deals` links the day deal on the asked
storefront. `product` returns the first 10 reviews as bol shows them, pooled
across the product family, with no reviewer names, plus bol's own AI review
topics. Deal products carry `seller_id` only. Not available: search
suggestions, review paging, seller review texts, price history or 30-day
lowest price, pickup points, bol Select member prices and a variant selector.
Failed calls are not charged; a not-found is charged.

### 56. Fashion -- Uniqlo prices by country, stock by size online and in stores, reviews with fit

Uniqlo in 41 markets. Namespace `uniqlo`, 12 endpoints: `search`,
`product`, `stock`, `store_stock`, `stores`, `reviews`, `suggestions`,
`category`, `deals`, `new_arrivals`, `categories`, `prices`. Pick the market
with `country` (default `us`) and the language with `language` (default the
market's local language). 1 credit per call; `store_stock` is 2 when resolved
from `product_id` + `color` + `size` (1 with `l2_id`), and `prices` is 1 per
market that answered. The request timeout is raised to at least 240s.

```python
from scavio import ScavioClient

client = ScavioClient()
uniqlo = client.uniqlo

# --- Uniqlo prices by country: one product id in up to 10 markets per call, each in its own currency.
p = uniqlo.prices("E479000-000")["data"]  # default jp, us, gb, de, fr, kr, au, ca, sg, th
for m in p["markets"]:
    print(m["country"], m["currency"], m["price"], m["promo_price"], m["on_sale"], m["title"])
print("not sold in:", p["not_sold"])

# --- On us, jp, kr and ca (and some items on sg, my, in) a drop is a FLAG: promo_price equals price there.
prod = uniqlo.product("E479000-000")["data"]
print(prod["title"], prod["price"], prod["promo_price"], prod["limited_offer"], prod["price_flags"])

# --- The same id on a European storefront, in its own language.
de = uniqlo.product("E479000-000", country="de", language="de")["data"]

# --- Online stock per colour x size, then one variant in the stores near a point.
st = uniqlo.stock("E479000-000")["data"]
print(st["variants_in_stock"], "/", st["variants_total"])
v = st["variants"][0]
print(v["l2_id"], v["color"]["name"], v["size"]["name"], v["status"], v["quantity"], v["quantity_capped"])
near = uniqlo.store_stock(40.758, -73.9855, l2_id="08665900", price_group="00")["data"]  # 1 credit; send the variant's price group
print(near["stores_with_stock"], "of", near["total_stores"])
same = uniqlo.store_stock(40.758, -73.9855, product_id="E479000-000", color="COL04", size="INS022")  # 2 credits

# --- Reviews with fit (1 tight .. 5 loose) and the purchased size.
rev = uniqlo.reviews("E479000-000", sort="most_helpful")["data"]
print(rev["rating"])
for r in rev["reviews"]:
    print(r["rating"], r["fit"], r["fit_label"], r["purchased_size"], r["height_range"], r["title"])

# --- Search, the category tree, one category, deals, new arrivals, stores and suggestions.
res = uniqlo.search("heattech", sort="price_asc")["data"]
print(res["total"], [(i["product_id"], i["title"], i["price"]) for i in res["items"][:3]])
tree = uniqlo.categories(gender="women")["data"]
jeans = uniqlo.category("22210,23296,23339")["data"]
offers = uniqlo.deals(type="limited_offer")["data"]
new = uniqlo.new_arrivals(country="jp", gender="men")["data"]
stores = uniqlo.stores(lat=40.758, lng=-73.9855)["data"]
print(uniqlo.suggestions("jea")["data"]["suggestions"])

# --- Greater China (tw, hk, cn): search + product, with Uniqlo's own codes there.
tw = uniqlo.search("牛仔褲", country="tw")["data"]
twp = uniqlo.product("u0000000055478", country="tw")["data"]
```

Markets by endpoint:
- **Every endpoint:** us (USD, en), jp (JPY, ja), kr (KRW, ko).
- **`search` + `product`:** tw (TWD), hk (HKD), cn (CNY), Uniqlo's Greater
  China sites, in Chinese, with their own product codes (not valid elsewhere).
- **`product` + `prices`:** au, be (nl, fr, en), ca (en, fr), de, dk (en), es,
  fr, gb (GBP; `uk` accepted), id, in, it, my, nl, ph, se (en), sg, th, vn, and
  Uniqlo's EU store (EUR, English) for at, bg, cz, ee, fi, gr, hr, hu, ie, lt,
  lu, lv, pl, pt, ro, si and sk.

Countries with no Uniqlo online store (ch, no, nz, mx, tr, ae, il, ru), a
market an endpoint does not serve and a language a market does not serve
answer 400 before anything is charged. The full list with currencies and
languages is in `product()`'s `country` docstring.

Product ids (`E479000-000`) are global on uniqlo.com, so `prices` compares
one id across markets in a single call. Prices are numbers in the market's
own currency, never converted. On us, jp, kr and ca (and on some items sg,
my and in) Uniqlo marks a drop with flags only, so `promo_price` equals
`price`; in Europe, Australia and most of Southeast Asia `promo_price` is
below `price`. `on_sale`, `limited_offer` and `price_flags` carry the flags.
Only a limited-time offer has a window: quote Uniqlo's own label in
`price_flags.name` (e.g. "until 11/18"), not a date read from `end`; a sale
flag carries a start but no end, and Select Colors/Sizes Only carries no
dates.

`price_group`: `product` and `prices` default to `"00"`, Uniqlo's regular
price list. Search can list the same `product_id` a second time in price
group `"01"`, mostly Uniqlo's Select Colors/Sizes Only sale price for some
colours / sizes; pass `price_group="01"` to `product` to read that price and
the colours / sizes it covers. `prices` compares group `"00"` unless
`price_group` is sent.

`stock` is online stock per variant (Uniqlo caps the quantity it shows at
11); `store_stock` is the status per store near a point, with no unit counts.
Send `store_stock` the price group the variant came from (`price_group`,
default `"00"`): a variant of price group 01 asked as 00 reads out of stock
in every store. Search
sorts are featured, newest, price_asc, price_desc and top_rated on us, jp,
kr, and best_selling instead of top_rated on tw, hk, cn. Review totals are
pooled per region (the European markets share one pool); reviews carry no
reviewer names or locations. No price history (poll `prices` and store your
own) and no store-level prices. GU is a separate brand and not a separate
platform here; Uniqlo's own listings can include GU collaboration items (kr
limited offers did). Failed calls are not charged; a not-found is charged.

### 57. Marketplace -- Depop resale prices, shop sold prices, shops and reviews

Depop (depop.com) across its 9 storefronts. Namespace `depop`, 14 endpoints:
`search`, `product`, `category`, `brand`, `explore`, `suggestions`, `shop`,
`shop_products`, `shop_sold`, `shop_reviews`, `shops_search`, `categories`,
`brands`, `similar`. Pick the buyer market with `country`: us (USD, the
default), gb (GBP; `uk` accepted), au (AUD), ie (EUR), ca (CAD), nz (NZD), de
(EUR), fr (EUR), it (EUR). `search`, `category`, `brand` and `explore` cost 1
credit (5 on nz); `product` 1 on us, 2 on gb, au, ie, ca, de, fr, it and 6 on
nz; everything else 1. The request timeout is raised to at least 240s
(storefront pages can take up to about a minute).

```python
from scavio import ScavioClient

client = ScavioClient()
depop = client.depop

# --- What listings ask in one buyer market: the first 24 results per query.
# Depop serves no next page: narrow with filters, sort or a price range.
res = depop.search("levis 501", country="gb", sort="price_asc", conditions=["used_excellent"])["data"]
print(res["count"], res["total_count"], res["currency"])
for item in res["items"][:3]:
    p = item["price"]  # numbers as a buyer in the market sees them; total = Scavio's sum of the parts
    # buyer_market_price False: priced in another currency, shown unconverted
    print(item["title"], item["buyer_market_price"], p["currency"], p["price"], p["buyer_fee"], p["tax"], p["shipping"], p["total"])

# --- One listing priced for a buyer in a market, plus the seller's own price.
# Listing ids are global: the same listing from another market shows that buyer's fee, tax and shipping.
# seller.country is the seller account's country (list items carry no seller country).
item = depop.product("f0omem-levis-550-38x36-blue-jeans-662f")["data"]
print(item["price"], item["listing_price"], item["seller"]["reviews_rating"], item["seller"]["items_sold"])

# --- What a shop's items sold for. Depop has no keyword sold search: sold prices come per shop,
# and Depop shows no sale date (updated_at is the listing's last update). status is "sold" (sold on
# Depop) or "marked_as_sold" (the seller marked it sold, which may be outside Depop).
sold = depop.shop_sold("flomem")["data"]
for s in sold["items"][:3]:
    print(s["title"], s["status"], s["price"]["price"], s["price"]["currency"], s["discount_percentage"], s["updated_at"])
more = depop.shop_sold("flomem", cursor=sold["next_cursor"]) if sold["has_more"] else None

# --- Shop profile, listings for sale, reviews (no reviewer names), shop search.
shop = depop.shop("flomem")["data"]
print(shop["reviews_rating"], shop["reviews_total"], shop["items_sold"], shop["last_seen"])
for_sale = depop.shop_products("flomem")["data"]
reviews = depop.shop_reviews("flomem", role="seller")["data"]
shops = depop.shops_search("y2k")["data"]["shops"]

# --- Category tree (paths feed category(), ids feed search filters), brands, browse.
tree = depop.categories(language="en")["data"]["departments"]
jeans = depop.category("mens/bottoms/jeans", country="de")["data"]
brands = depop.brands("c")["data"]["brands"]          # slug feeds brand(), id feeds brand_ids
carhartt = depop.brand("carhartt", sort="price_desc")["data"]
nineties = depop.explore("90s-menswear")["data"]      # more_slugs lists the market's other pages
hints = depop.suggestions("carh")["data"]["suggestions"]
similar = depop.similar(1002884801)["data"]["items"]  # us only
```

Markets per endpoint: `search`, `product`, `category`, `brand`, `explore` and
`suggestions` on all nine; `similar` us only; `shop`, `shop_products`,
`shop_sold`, `shop_reviews`, `shops_search`, `categories` and `brands` are
global (no `country`). Any other country answers 400 before anything is
charged.

The market is the buyer's country: search shows that market's sellers, and
prices are what a buyer there pays as Depop shows them (`price`,
`original_price`, `buyer_fee`, `tax` with `tax_type`, `shipping` with
`shipping_boundary`, `total` (Scavio's sum of price, buyer fee, tax and
shipping), `headline_price` (the price Depop itself headlines: us leaves out
shipping, gb includes the fee and shipping)). `original_price` is the
seller's own original price and can be far above `price`; `shipping` is what
the buyer pays (product's `shipping.national_cost` is the seller's domestic
rate and can differ). `price.currency` is the listing's currency: usually the
market's, but some sellers list in another one; list items carry
`buyer_market_price`, False for those, which Depop shows unconverted (product
too). List items carry no seller country; product has `seller.country`. On us, Depop returns a buyer fee on some calls and not on others for the
same listing, so read what comes back. Sorts are relevance, `price_asc` and
`price_desc` (newest and most popular are not available). Depop's interface
is English in every storefront; titles and descriptions are what sellers
wrote (often German, French or Italian on de, fr, it), and `categories`
answers group and product type names in en, en-US, de, fr or it. Not
available: results past the first 24, keyword sold search, trending
searches, views, join date, Top Seller badge, offers / bundles, price history,
`similar` outside us. Failed calls are not charged; a not-found is charged.

### 58. Marketplace -- Poshmark sold prices, listings, closets and Love Notes

Poshmark on poshmark.com (us, USD) and poshmark.ca (ca, CAD); both
storefronts are English. Namespace `poshmark`, 15 endpoints: `search`,
`sold`, `product`, `category`, `brand`, `closet`, `closet_listings`,
`love_notes`, `closets_search`, `categories`, `brands`, `suggestions`,
`parties`, `party_listings`, `similar`. Pick the market with `country` (us is
the default). 1 credit per call on every endpoint. The request timeout is
raised to at least 240s.

```python
from scavio import ScavioClient

client = ScavioClient()
posh = client.poshmark

# --- Sold prices by keyword: the price shown on the sold listing and the date Poshmark
# marked it sold. Up to 480 sold listings per query and filter combination (10 pages of 48):
# narrow with filters or split by price range to reach more.
sold = posh.sold("coach bag", department="Women", category="Bags", condition="good")["data"]
print(sold["count"], sold["total"], sold["currency"], sold["has_more"])
for item in sold["items"][:3]:
    print(item["title"], item["price"]["amount"], item["price"]["currency"], item["sold_at"])
under_100 = posh.sold("coach bag", price_max=100, page=2)["data"]

# --- Active listings: original price the seller entered, first price and price drops.
res = posh.search("lululemon align", country="ca", sort="price_drop")["data"]
for item in res["items"][:3]:
    print(item["title"], item["price"], item["original_price"], item["first_price"], item["price_drop_percent"])

# --- One listing in full (listing ids are global: it opens from either market in its own currency).
listing = posh.product("6ad80f0dce5b0ace7ee9abd7")["data"]
print(listing["price"], listing["shipping"], listing["seller"]["items_sold"], listing["seller"]["love_notes"])

# --- Closets: stats, listings (available or sold) and the latest 100 Love Notes.
closet = posh.closet("thriftedbyher")["data"]
print(closet["posh_ambassador"], closet["followers"], closet["items_sold"], closet["orders_shipped"])
closet_sold = posh.closet_listings("thriftedbyher", availability="sold")["data"]
notes = posh.love_notes("thriftedbyher")["data"]
print(notes["count"], notes["total"], notes["notes"][0]["comment"])
closets = posh.closets_search("vintage")["data"]["closets"]

# --- Browse: category tree, category and brand grids, top brands, suggestions, parties, similar.
tree = posh.categories()["data"]["departments"]
bags = posh.category("Women", category="Bags", availability="sold")["data"]
coach = posh.brand("Coach", sort="just_in")["data"]
top = posh.brands()["data"]["brands"]
hints = posh.suggestions("lulu")["data"]["suggestions"]
parties = posh.parties(status="scheduled")["data"]["parties"]
if parties:
    shared = posh.party_listings(parties[0]["party_id"])["data"]
similar = posh.similar("6ad80f0dce5b0ace7ee9abd7")["data"]["items"]
```

Search, sold, category, brand, brands, suggestions, parties, party listings
and similar return that market's own listings in its currency. Listing ids
and closets are global: a listing opens from either market in its own
currency (no conversion), and closet listings are read in the seller's home
market. Any other country answers 400 before anything is charged.

On a sold listing, `price` is the price shown on the sold listing (Poshmark
says a sold listing reflects the final order price; offers are private and
not returned) and `sold_at` is the date Poshmark marked it sold.
`original_price` is the original price the seller entered; `first_price` is
the price it was first listed at, which can be below `price` when the seller
raised the price. `total` is Poshmark's approximate count; active search
reaches about 5,000 listings per query (105 pages of 48), sold search 480 per
query and filter combination. Conditions: `new_with_tags`,
`new_with_tags_or_boutique`, `boutique`, `like_new`, `good`, `fair`. Sorts:
relevance, `just_shared`, `just_in`, `price_asc`, `price_desc`,
`price_drop`, `most_liked`. `items_sold` is Poshmark's display string (e.g.
`700+`). Seller usernames only: no real names, cities, likers, comment
authors or Love Note buyers. Not available: sold results beyond 480 per query
and filter combination, Love Notes beyond the latest 100, Posh Shows,
trending searches, the full brand directory (top 50; brand inputs take any
name), offers, bundles, price history. Failed calls are not charged; a
not-found is charged.

### 59. Marketplace -- thredUP prices, estimated retail, sold listings and deals

thredUP's US store (thredup.com, English, USD; thredUP ships to the US and
Canada from it), so there is no `country` param. Namespace `thredup`, 12
endpoints: `search`, `sold`, `product`, `category`, `brand`, `deals`,
`rescue_boxes`, `categories`, `brands`, `suggestions`, `trending`,
`similar`. 1 credit per call on every endpoint. List calls take 15 to 45
seconds; the request timeout is raised to at least 240s.

```python
from scavio import ScavioClient

client = ScavioClient()
tu = client.thredup

# --- Prices: the price, the estimated original retail, % off, condition and who priced it.
res = tu.search("denim jacket", seller_type="thredup", condition=["excellent", "new_with_tags"])["data"]
print(res["sort"], res["count"], res["total"], res["total_capped"], res["has_more"])
for item in res["items"][:3]:
    print(item["title"], item["price"], item["estimated_retail"], item["percent_off"], item["seller_type"], item["condition"])

# --- One item in full: the flaws thredUP noted, measurements, materials, characteristics.
item = tu.product(241601590)["data"]
print(item["price"], item["estimated_retail"], item["percent_off"], item["condition_notes"], item["measurements"], item["materials"])

# --- Sold listings: filters only (brand and / or category, no keyword), with the price the
# item last listed at. thredUP shows no sold date.
sold = tu.sold(brand="Coach", department="handbags")["data"]
for s in sold["items"][:3]:
    print(s["title"], s["price"], s["estimated_retail"], s["condition"], s["status"])

# --- Category and filter values: sizing ids feed `size`, tags feed `category`.
cats = tu.categories(department="women")["data"]
small = [s["size"] for s in cats["sizes"] if s["label"] == "S"]
dresses = tu.category("women", "dresses", size=small, sort="price_low")["data"]

# --- Brands, deals, Rescue boxes, suggestions, trending, similar.
coach = tu.brands(query="coach")["data"]["brands"]
madewell = tu.brand("Madewell", category="jeans")["data"]
clearance = tu.deals("clearance", department="women")["data"]
drops = tu.deals("price_drops", brand="Madewell")["data"]
boxes = tu.rescue_boxes()["data"]["boxes"]
for box in boxes[:2]:
    print(box["name"], [(b["items"], b["price"], b["state"]) for b in box["bundles"]])
hints = tu.suggestions("made")["data"]["suggestions"]
trending = tu.trending()["data"]["searches"]
similar = tu.similar(241601590)["data"]["items"]
```

`estimated_retail` is the estimated original retail: thredUP's own estimate
on items thredUP prices, entered by the seller on Direct Listing items.
`percent_off` is computed from the price and the estimated retail
(`round((1 - price / estimated_retail) * 100)`), `None` when the estimated
retail is missing or not above the price. `seller_type` is `thredup`,
`direct_listing` (peer sellers) or `dropship` (partner listings); `status`
is `available`, `reserved` or `sold`. Conditions: `new_with_tags`,
`excellent`, `very_good`, `good`, `flawed`. Departments: `women` (default),
`girls`, `boys`, `handbags`, `shoes`, `designer`, `plus`, `juniors`,
`maternity`, `accessories`; thredUP has no men's department.

List endpoints answer 119 items per page, pages 1 to 21 (about 2,500 items
per query and filter combination); `total` caps at 10,000 (`total_capped`
True means 10,000+). Free text is matched loosely (semantic), so use `brand`
for one brand. `size` takes sizing ids from `categories`, not labels;
`condition`, `color` and `material` take up to 5 values. The price filter
is approximate (thredUP matches a base price). Every answer reports the
`sort` applied: `default`, `recommended`, `relevance`, `newest`,
`price_high`, `price_low`, `price_drop`. Not available: product reviews
(thredUP shows none), seller shops, sold dates, men's clothing, price
history. No seller or consignor names or ids are returned. Failed calls are
not charged; a not-found is charged.

### 60. Fashion -- Fashion Nova sale prices, compare-at prices, sizes in stock, reviews

Fashion Nova in 104 countries. Namespace `fashionnova`, 7 endpoints:
`search`, `product`, `collection`, `categories`, `suggestions`, `reviews`,
`similar`. 1 credit per call on every endpoint. Pick the storefront with
`country` (default `us`) and the language with `language` (`en` default,
`es` in 67 countries). Review calls take 20 to 60 seconds; the request timeout
is raised to at least 240s on every endpoint.

```python
from scavio import ScavioClient

client = ScavioClient()
fn = client.fashionnova

# --- Sale prices: price, compare-at (struck-through) price, percent off, final sale, sizes in stock.
res = fn.search("bodycon dress", country="us", sort="best_selling")["data"]
print(res["currency"], res["total"], res["total_pages"], res["has_more"])
for item in res["items"][:3]:
    print(item["title"], item["price"], item["compare_at"], item["percent_off"],
          item["final_sale"], item["sizes_in_stock"])

# --- One style in one colour: every size with its SKU, price, compare-at and quantity.
jeans = fn.product("san-diego-sculpting-stretch-flare-jeans", color="black-wash", country="gb")["data"]
print(jeans["currency"], jeans["price"], jeans["compare_at"], jeans["percent_off"], jeans["promo"])
for size in jeans["sizes"][:3]:
    print(size["size"], size["sku"], size["price"], size["quantity"], size["low_stock"])
print(jeans["rating"], jeans["site_ai_review_summary"])  # Fashion Nova's own AI review summary

# --- Spanish storefront: titles, descriptions and attributes in Spanish, prices in MXN.
mx = fn.product("san-diego-sculpting-stretch-flare-jeans", country="mx", language="es")["data"]

# --- Collections (up to about 10,000 products, pages 1-166): sale, best-sellers, new, back-in-stock ...
sale = fn.collection("sale", country="ca", filters={"occasion": "Vacation"})["data"]
print(sale["total"], sale["total_pages"], sale.get("unrecognized_filters"))

# --- Navigation (collection handles), suggestions, reviews (one pool per style), similar (US store).
tree = fn.categories(division="women")["data"]["categories"]
hints = fn.suggestions("dress")["data"]["queries"]
reviews = fn.reviews("san-diego-sculpting-stretch-flare-jeans", sort="most_recent", star=5)["data"]
for r in reviews["reviews"][:3]:
    print(r["rating"], r["title"], r["fit"], r["size_purchased"], r["usual_size"])
similar = fn.similar("san-diego-sculpting-stretch-flare-jeans", limit=24)["data"]["items"]
```

Markets: the 104 countries in Fashion Nova's own country selector, each in
its own currency (37 currencies: us USD, ca CAD, gb GBP, au AUD, mx MXN, jp
JPY, ae AED, the euro countries EUR ...; `zz` is the site's International
storefront in USD). `language="es"` is served in 67 countries (not the US
store). A country or language Fashion Nova does not run answers 400 before
anything is charged. `categories` and `suggestions` are the same in every
storefront, `reviews` is one pool per style (not per colour) shared by every
market and mostly English (no `country`; `language` per review says which;
`size_purchased` / `usual_size` are the reviewer's free text), and `similar`
answers from the US store in USD.

Prices are numbers in the storefront's currency, never converted: `price`
(the lowest size price), `compare_at` (the site's struck-through price),
`percent_off` (computed by Scavio: `round((1 - price / compare_at) * 100)`),
`on_sale`, `price_with_code` (the price with Fashion Nova's current code as
the page computes it, 40% off the compare-at price), `code_lowers_price`
(`False` when that code price is not below `price`: the code does not lower
it; `None` without a code price) and `final_sale`. `badge` is the site's label
and can read a different percent than the computed `percent_off`. In the 27 EEA countries (at, be, cy, cz,
de, dk, ee, es, fi, fr, gr, hu, ie, is, it, lt, lu, lv, mt, nl, no, pl, pt,
ro, se, si, sk) Fashion Nova shows VAT-inclusive prices and no compare-at
price, so `compare_at` and `percent_off` are `None` there. The same jeans read
on 2026-11-19: us 18 USD (compare-at 34.99, 49% off), ca 27 CAD (51), gb 17
GBP (32), au 31 AUD (60), mx 338 MXN (656), fr 20.95 EUR (no compare-at).
`sizes[].quantity` is the stock Fashion Nova's page shows per size, not a
guaranteed inventory count.

`search` is semantic and matched loosely: its `total` moves between calls, a
later page can repeat a few items, and it shows its first 18 pages of 60 (6
under a sort other than `featured`); narrow with filters. `collection` lists
up to about 10,000 products (pages 1 to 166; `total` can be larger,
`total_pages` is approximate, `has_more` follows the site's page count), and
consecutive pages can repeat a few products: dedupe by `product_id` + `color`.
Filters: `size`, `color`, `price_min` / `price_max` (whole units of the
storefront's currency), `division` (`women`, `curve`), `category`, and
`filters` for any other facet by `facets[].name`; a facet the list does not
offer matches nothing and is listed in `unrecognized_filters` (present only
then). Sorts:
`featured`, `best_selling`, `price_low`, `price_high`, `newest`. `reviews`:
`highest_rated` (default), `most_recent`, `most_helpful`, `lowest_rated`,
`star` 1-5, 10 per page, pages 1 to 8, totals as returned; reviewer names are
never returned. Not available: stores (Fashion Nova lists none), a brand
directory or brand filter (`brand` is the store's vendor field; collab and
licensed brand names appear in titles), price history (poll and store the
answers), gift cards, new-arrival dates. Failed calls are not charged; a
not-found is charged.

### 61. Retail -- Argos store stock, prices, was prices, reviews

Argos (argos.co.uk, UK, GBP). Namespace `argos`, 10 endpoints: `search`,
`product`, `store_stock`, `stores`, `reviews`, `questions`, `categories`,
`category`, `deals`, `suggestions`. 2 credits per call on every endpoint. One
store, so there is no `country` (Argos Ireland closed in 2023). The request
timeout is raised to at least 240s on every endpoint.

```python
from scavio import ScavioClient

client = ScavioClient()
ar = client.argos

# --- Store stock: which Argos stores near a UK postcode can hand over each product, and when.
stock = ar.store_stock(["8377058", "7163184"], "SW1A 1AA")["data"]
for store in stock["stores"][:3]:
    print(store["name"], store["type"], store["distance_miles"])
    for p in store["products"]:
        print("  ", p["product_id"], p["state"], p["available_from"])  # e.g. collect_tomorrow
for p in stock["delivery"]["products"]:
    print(p["product_id"], p["state"], p["fast_track"])  # e.g. next_day

# --- Prices: price, was price, save (computed), the site's offer text and badges.
res = ar.search("air fryer", seller="argos", sort="price_low")["data"]
print(res["total"], res["total_pages"], res["page_size"], res["tu_clothing_excluded"])
for item in res["items"][:3]:
    print(item["name"], item["price"], item["was_price"], item["save"], item["offer_text"],
          item["badges"], item["seller"])

# --- One product: EAN, badges with dates, specs, variants, care plans, first 10 reviews.
kettle = ar.product("8377058")["data"]
print(kettle["template"], kettle["ean"], kettle["price"], kettle["was_price"], kettle["badges"])

# --- Reviews: up to 100 per page, 5 sorts, star filter, syndicated reviews flagged.
reviews = ar.reviews("7163184", sort="most_helpful", rating=[1, 2], limit=100)["data"]
print(reviews["total"], reviews["summary_source"], reviews["summary"])  # Argos's own AI summary
for r in reviews["reviews"][:3]:
    print(r["rating"], r["title"], r["syndicated"], r["syndication_source"])

# --- Stores, Q&A, departments, categories, deal collections, suggestions.
stores = ar.stores("M1 1AE")["data"]["stores"]
one = ar.stores(store=stores[0]["store"])["data"]
qa = ar.questions("8377058")["data"]["questions"]
tree = ar.categories()["data"]["departments"]
kettles = ar.category("29560", sort="rating")["data"]
bf = ar.deals("black_friday")["data"]
top = ar.deals("top_100", page=1)["data"]
hints = ar.suggestions("lego")["data"]["suggestions"]
```

Store stock is availability, not unit counts. Each store answers a collection
state per product: `collect_now`, `collect_today`, `collect_tomorrow`,
`collect_later`, `out_of_stock`, `not_available`, with `available_from` and the
site's message; `delivery` answers `same_day` (Fast Track), `next_day`,
`later` (Argos's "Delivery within N days", with `days`), `out_of_stock` or
`not_available`; quote delivery from `state` and `message` (`available_from`
is the date Argos returns, as given). `postcode` is where stores are
searched (up to 10 stores within 50 miles); `delivery_postcode` (default
`postcode`) is where delivery is checked. Store types: `argos_store` (a
standalone Argos store), `inside_sainsburys` (an Argos counter inside a
Sainsbury's store), `collection_point` (a collect-only point, no shop). Trusted Seller items are never
stocked in stores (400).

Prices are numbers in GBP as Argos shows them: `price`, `was_price` (the
site's was price), `save` (computed by Scavio as `was_price - price`),
`offer_text` (the site's own words, e.g. Half Price) and `badges` as given
(e.g. `Black_Friday`, `price_guarantee`). `seller` is `argos` or
`trusted_seller` (Argos's marketplace; the page names no seller, so
`seller_name` is `None` there). `search`, `category` and `deals` return 24 per
page, pages 1 to 200 (`total_pages` says how deep the list goes; `top_100` is
2 pages of 60; Argos stops counting at 10,000, flagged by `total_capped`); Tu Clothing items are left out and counted in
`tu_clothing_excluded`. Filters: `brand`, `category`, `seller`, `offers`,
`new_in`, `colour`, `price_min` / `price_max`, `rating_min` and `filters` (any
facet by `facets[].name`); sorts `relevance`, `price_low`, `price_high`,
`rating`. `reviews`: `newest` (default), `oldest`, `most_helpful`,
`highest_rating`, `lowest_rating`, `rating` star filter, up to 100 per page
with every review reachable; reviewer names, locations, ages and genders are
never returned. Not available: unit counts, price history (poll and store the
answers), a brand directory (brand is a filter), Argos Ireland, card or
checkout prices, Argos Pay terms. Failed calls are not charged; a not-found is
charged.

### 62. Retail -- Media Expert Black Week prices, Omnibus 30-day low, store stock

Media Expert (mediaexpert.pl, Poland, PLN). Namespace `mediaexpert`, 13
endpoints: `search`, `product`, `store_stock`, `stores`, `reviews`,
`category`, `categories`, `brands`, `brand`, `promotions`, `outlet`, `seller`,
`suggestions`. Billed on actual cost, 1 to 3 credits per call
(`credits_used` reports each one). One store, so there is no `country`;
names, specifications, labels and reviews come back in Polish, as Media
Expert writes them. The request timeout is raised to at least 240s on every
endpoint.

```python
from scavio import ScavioClient

client = ScavioClient()
me = client.mediaexpert

# --- Prices: price, old price, the Omnibus 30-day low Media Expert shows, the code price.
p = me.product("8128227")["data"]
print(p["name"], p["price"], p["old_price"], p["omnibus_lowest_30d"], p["currency"])
print(p["code_price"], p["discount_shown"], p["discount_percent"])  # code_price: {price, code, valid_from, valid_to} or None

# --- Store stock: Media Expert's stock indicator at the 40 stores nearest a city or postcode.
stock = me.store_stock("8128227", "Warszawa")["data"]
print(stock["count"], stock["in_stock_count"], stock["collect_in_1h_count"])
for s in stock["stores"][:3]:
    print(s["name"], s["distance_km"], s["stock_level"], s["collect_in_1h"], s["order_to_store_day"])

# --- Search: 30 per page (up to 50); many single words redirect to a category page.
res = me.search("telewizor")["data"]
print(res["redirected_to"], res["total"], res["total_capped"], res["page_size"])
for item in res["items"][:3]:
    print(item["product_id"], item["name"], item["price"], item["old_price"],
          item["omnibus_lowest_30d"], item["code_price"], item["seller"])

# --- Reviews by sku (items[].sku): up to 100 per page, verified-purchase and promotional flags.
reviews = me.reviews("709727", sort="newest", verified=True, limit=100)["data"]
print(reviews["total"], reviews["average_rating"], reviews["verified_purchases"])
for r in reviews["reviews"][:3]:
    print(r["rating"], r["title"], r["verified_purchase"], r["incentivized"])

# --- Black Weeks promotion lists, categories, brands, outlet, marketplace sellers, stores.
lists = me.promotions(black_weeks=True)["data"]["lists"]
bw = me.promotions(lists[0]["list"])["data"]
tree = me.categories(depth=2)["data"]["categories"]
washers = me.category("agd/pralki-i-suszarki/pralki", filters=["bosch"])["data"]
brands = me.brands("sams")["data"]["brands"]
samsung = me.brand("samsung")["data"]
outlet = me.outlet()["data"]
seller = me.seller("autobi")["data"]
stores = me.stores("Warszawa")["data"]["stores"]
hints = me.suggestions("pral")["data"]["suggestions"]
```

Credits, as `credits_used` reports them: `product`, `stores`, `brands`,
`reviews` and `suggestions` cost 1; `store_stock` and `categories` cost 2;
`search` costs 3 for a search page (Media Expert loads search lists lazily,
so the rest of the page takes one more lookup) or 1 when Media Expert answers
the term with a full category page; `category`, `brand`, `outlet`, `seller`
and a promotion list's products cost 1 unsorted and 3 with a sort or a lazily
loaded list (the promotion lists themselves and the outlet's groups cost 1).

Prices are numbers in PLN: `price`, `old_price` (Media Expert's
struck-through price), `omnibus_lowest_30d` (the lowest price of the last 30
days that Media Expert shows next to a promotion, under the EU Omnibus
Directive), `code_price` `{price, code, valid_from, valid_to}` (the price with
a discount code), `discount_shown` (Media Expert's own figure) and
`discount_percent` (computed by Scavio). Store stock is Media Expert's stock
indicator, a bucket (seen: 0, 2, 9, 20), not a unit count, with
`collect_in_1h` (Odbierz za godzinę) and `order_to_store_day` when the item is
not on the shelf. Send `product_id`, not `offer_id` (an offer id is refused
before anything is charged); marketplace items (sold and shipped by a
marketplace seller, `seller.marketplace` True) are never stocked in stores (a
charged 400) and have no Media Expert reviews. Lists return 30 per page by
default (`limit` 5, 10, 15, 20, 30 or 50), up to 100 pages, and stop counting
at 5,000 (`total_capped`). Price sorts are Media Expert's own order, which
follows promotional and code prices, so re-sort a page for a strict order.
There is no price filter; `filters` takes `facets[].values[].filter`.
`reviews`: `most_helpful` (default), `least_helpful`, `newest`, `oldest`,
`highest_rating`, `lowest_rating`, `rating_min` / `rating_max`, `verified`;
no reviewer identity is returned. Not available: Q&A (Media Expert has none),
leaflets, price history (poll and store the answers), unit counts, checkout
prices, other countries or languages. Failed calls are not charged; a
not-found is charged.

### 63. Retail -- Action weekly deal prices by country, stores and opening hours

Action (action.com), the European non-food discount store, on 19 storefronts
in 16 countries. Namespace `action`, 16 endpoints, 1 credit each: `search`,
`product`, `products`, `category`, `categories`, `brand`, `brands`,
`new_arrivals`, `weekly_deals`, `collection`, `suggestions`, `stores`,
`store`, `reviews`, `webshop_search`, `webshop_product`. Every endpoint takes
`country` (nl by default, be, fr, lu, de, at, ch, it, es, pt, pl, cz, sk, ro,
hr, si) and, for be and ch, `language` (be nl or fr; ch de, fr or it). The
request timeout is raised to at least 240s on every endpoint.

```python
from scavio import ScavioClient

client = ScavioClient()
ac = client.action

# --- This week's deals: Action's week id and validity dates (Wednesday to Tuesday).
deals = ac.weekly_deals()["data"]
print(deals["week_id"], deals["label"], deals["valid_from"], deals["valid_to"], deals["total"])
for item in deals["items"][:3]:
    print(item["product_code"], item["title"], item["price"], item["regular_price"],
          item["deal"]["valid_to"])

# --- One article number everywhere, priced per market: one call per country.
codes = ["3225277", "3011615", "3225488"]
for country in ("nl", "de", "pl"):
    res = ac.products(codes, country=country)["data"]
    print(country, res["currency"], res["not_sold"],
          [(i["product_code"], i["price"]) for i in res["items"]])

# --- The 20 stores nearest a city or postcode, with 7 dated days of opening hours (no stock).
stores = ac.stores("Amsterdam")["data"]
for s in stores["stores"][:3]:
    print(s["store_id"], s["name"], s["country_code"], s["address"]["postcode"], s["hours"][0])
one = ac.store(stores["stores"][0]["store"])["data"]

# --- Search, one product, reviews (nl, de, fr, pl only), the webshop (nl and be only).
res = ac.search("kerst", sort="price_asc")["data"]
p = ac.product("3225277", country="be", language="fr")["data"]
reviews = ac.reviews("3224838", scope="all", sort="newest")["data"]
web = ac.webshop_search("stofzuiger")["data"]
ean = ac.webshop_product(web["items"][0]["ean"])["data"]
print(ean["stock_level"], ean["order_limit"], ean["shipping_cost"], ean["availability"])

# --- Categories, own brands, new arrivals, the Black Friday collection, suggestions.
tree = ac.categories(depth=2)["data"]["categories"]
home = ac.category("wonen/woonaccessoires")["data"]
brands = ac.brands()["data"]["brands"]
max_more = ac.brand("max-more")["data"]
new = ac.new_arrivals(country="de")["data"]
bf = ac.collection("black-friday")["data"]
hints = ac.suggestions("opberg")["data"]["suggestions"]
```

Prices are numbers in the market's currency (EUR; CHF on ch, PLN on pl, CZK
on cz, RON on ro), never converted: `price`, `regular_price` (Action's
struck-through price), `unit_price` (as shown), `discount_percent` (computed by
Scavio) and `price_note` (Action's note on the struck-through price, e.g. the
EU 30-day lowest price in Poland). Article numbers (`product_code`) are the
same in every market and prices are set per market. Titles and labels come
back in the storefront's language, as Action writes them (Dutch on the default
nl storefront). Lists return 24 products a page (23 on weekly deals) up to page
200, with `total` and `total_pages`; sorts `relevance`, `price_asc`,
`price_desc`, `newest`; filters `category_filter`, `price_range`,
`brand_filter`, `new_only` take values from `facets`.

`weekly_deals`: `week_id` (e.g. Promo2026Week47), Action's `label` and ISO
`valid_from` / `valid_to` dates; a deal week runs Wednesday to Tuesday and the
assortment changes weekly; Belgium adds Action Plus `loyalty_deals`. `brands`
lists Action's own brands (about 54 private labels). `stores` gives the 20
nearest stores to a city, postcode or `lat` / `lng` (they may cross a border:
`country_code` per store; `distance_km` only for `lat` / `lng`). Action does not
publish store stock. `reviews` exist on nl, de, fr and pl only (other countries
answer 400, not charged), scope `local` (default, that storefront's language),
`international` or `all` (`offset + limit` up to 100); no reviewer identity is
returned. `webshop_search` and `webshop_product` read shop.action.com (nl-nl,
nl-be, fr-be): EAN, online `stock_level` (not store stock), `order_limit`,
`shipping_cost`, release and end dates; EANs come only from the webshop. Not
available: store stock, price history (poll and store the answers), leaflets,
checkout, other countries. Failed calls and refused inputs are not charged; a
not-found (an article the market does not sell, an unknown slug or EAN) is
charged.

### 64. Retail -- HEMA store stock, dated promotions and prices by market

HEMA (hema.com), the Dutch variety store, on its four webshops (nl, be in
Dutch or French, fr, de), with stores also in Luxembourg and Austria.
Namespace `hema`, 13 endpoints, 1 credit each: `search`, `product`,
`category`, `categories`, `new_arrivals`, `sale`, `offers`, `campaign`,
`suggestions`, `store_stock`, `stores`, `store`, `reviews`. Every endpoint but
`store` takes `country` (nl by default, be, fr, de; lu and at only on
`store_stock` and `stores`) and, for be, `language` (nl or fr). The request
timeout is raised to at least 240s on every endpoint.

```python
from scavio import ScavioClient

client = ScavioClient()
hm = client.hema

# --- HEMA store stock: sellable units per store for up to 12 articles near a city or postcode.
st = hm.store_stock(["15300147", "10860090"], query="Utrecht")["data"]
print(st["location"]["formatted_address"], st["summary"])
for s in st["stores"][:3]:
    print(s["store_id"], s["name"], s["distance_km"],
          [(x["sku"], x["sellable_units"], x["stock_level"]) for x in s["stock"]])

# --- One article in full: EAN, variants and the dated price schedule with upcoming promotions.
p = hm.product("15300147")["data"]
print(p["ean"], p["price"], p["promotion"])
for row in p["price_schedule"]:
    print(row["valid_from"], row["valid_to"], row["price"], row["promotion"])

# --- One article number everywhere, priced per market: one call per country.
for country in ("nl", "be", "fr", "de"):
    print(country, hm.product("15300147", country=country)["data"]["price"])

# --- Weekly offers (nl, be): the validity label, ISO date, week and promotion cards.
offers = hm.offers()["data"]
print(offers["label"], offers["valid_to"], offers["week"], offers["section_count"])

# --- Search, a category, campaigns, stores, one store, reviews.
res = hm.search("bougie", country="be", language="fr", sort="price_asc")["data"]
baby = hm.category("baby/babykleding", filters={"maincolour": "zwart"})["data"]
xmas = hm.campaign("christmas", country="de")["data"]
stores = hm.stores("Utrecht")["data"]["stores"]
one = hm.store("0013", sku="15300147")["data"]
reviews = hm.reviews("10860090", sort="highest")["data"]
print(reviews["review_pool"], reviews["total_text_reviews"], reviews["total_ratings"])
```

Prices are numbers in EUR: `price`, `was_price` (HEMA's struck-through
price, as shown), `price_from` (a from-price across sizes or colours),
`unit_price` and `discount_percent` (computed by Scavio from the was price).
Names, labels and promotion texts come back in the market's language, as HEMA
writes them (Dutch on the default nl market, e.g. "2+1 gratis"). Article
numbers (`sku`) are the same in every market and prices are set per market;
HEMA notes that online prices can differ from store prices. Lists return 24
products a page up to page 100, with `total` and `total_pages`; sorts
`relevance`, `price_asc`, `price_desc`, `newest`, `best_selling` (a from-price
tile is placed by one of its variants' prices); `filters` take
`{facets[].facet: value or [values]}` (up to 6), plus `new_only`, `price_min`
and `price_max`. A keyword HEMA sends to a landing page (e.g. kerst) comes back
as that page's product carousels with `redirected_to` set.

`product` returns the EAN, colour / size variants with stock flags, the dated
`price_schedule` (upcoming promotions included), online stock,
`sellable_in_store` and the order limit. `store_stock` gives, per store, the
sellable units HEMA's store service reports and the stock level (full,
regular or limited), shelf locations, hours, address and distance: stock as
HEMA reports it, not a promise that the shelf has it. `stores` lists a
country's stores or the ones near a place; `store` reads one store by id (any
HEMA country), with one article's stock when `sku` is given. `offers` (nl, be)
returns HEMA's validity label as shown, the ISO `valid_to`, the week and the
promotion cards with their list paths (no products on that page). `campaign`
takes `christmas` (all markets) or `sinterklaas` (nl, be). `sale` serves nl,
be and de (France has none). `reviews` are HEMA's own product reviews, pages 1
to 5 (8, then 30 more a page), sorted `newest` or `highest`; nl, fr and de read
the Dutch pool, be its own; no reviewer identity is returned. No brands
endpoint (HEMA sells its own brand). Not available: price history (poll and
store the answers), checkout or ordering, the photo service and cake
ordering, other countries (no UK or Spain). Failed calls and refused inputs
are not charged; a not-found (an article number HEMA does not have, an
unknown store id, a place the store finder cannot find) is charged.

### 65. Auto Parts -- AutoZone parts prices by vehicle, core charges, warranty, stores

AutoZone (autozone.com), the US auto parts retailer, plus autozone.com.br and
autozone.com.mx. Namespace `autozone`, 12 endpoints: `search`, `product`,
`category`, `brand`, `vehicles`, `reviews`, `stores`, `store`, `categories`,
`clearance`, `rebates`, `store_stock`. 1 credit per call; 2 on `search` and
`product` with `country="br"` and on `store_stock` (Brazil only). `country` is
us by default; br on `search`, `product`, `vehicles`, `stores`, `store` and
`categories`; mx on `vehicles`, `stores`, `store` and `categories` only.
`category`, `brand`, `reviews`, `clearance` and `rebates` are us only and take
no `country`. The request timeout is raised to at least 240s on every
endpoint.

```python
from scavio import ScavioClient

client = ScavioClient()
az = client.autozone

# --- Parts that fit one vehicle: the same part type unfiltered, then for a 2018 Ford F-150.
pads = az.category("/brakes-and-traction-control/brake-pads")["data"]
fit = az.category("/brakes-and-traction-control/brake-pads",
                  vehicle={"year": 2018, "make": "Ford", "model": "F-150"})["data"]
print(pads["total"], fit["total"], fit["priced_for"])
for it in fit["items"][:3]:
    print(it["part_number"], it["name"], it["price"], it["core_charge"], it["warranty"],
          it["fitment"]["vehicle_fit"])

# --- Vehicle names come from the selector, one level at a time.
makes = az.vehicles(level="makes", year=2018)["data"]["makes"]
models = az.vehicles(level="models", year=2018, make_id=54)["data"]["models"]

# --- Another brand's part number finds the parts AutoZone matches to it.
xref = az.search("PH3614")["data"]
print(xref["total"], xref["oem_part_number"], xref["oem_brand"])

# --- One product in full: price, deal, core charge, warranty, pickup and ratings.
p = az.product("1399158")["data"]
print(p["priced_for"], p["price"], p["deal_price"], p["core_charge"], p["warranty"])
print(p["availability"]["store_pickup"], p["rating"]["average"])

# --- Reviews, the store directory, one store, clearance and rebates.
reviews = az.reviews("1399158", sort="most_recent")["data"]
states = az.stores()["data"]["states"]
houston = az.stores(state="tx", city="houston")["data"]["stores"]
barre = az.store("vt/barre/18-overlook-dr.html")["data"]
rebates = az.rebates()["data"]["rebates"]

# --- Brazil: search and one product at a Brazilian store you choose (BRL, Portuguese text).
br = az.search("pastilha de freio", country="br")["data"]
stock = az.store_stock("9403", id="100112748")["data"]
print(stock["priced_for"], stock["price"], stock["in_store"])
```

Every price is AutoZone's price for the store AutoZone assigns to the request,
named in `priced_for` (`store_number`, `address`, `city`, `state`, `zip`).
AutoZone prices differ by store, core charges too, so the same part can cost
more or less elsewhere and two calls can be priced for different stores; there
is no store or ZIP input on us. Items carry `price`, `was_price` (AutoZone's
struck-through price, as shown), `deal_price`, `discount_percent` (computed by
Scavio from the was price), `core_charge` (the refundable deposit AutoZone adds
on parts like batteries until the old part is returned; 0 when none),
`warranty` and availability per fulfilment option (store pickup, ship to home,
next day, same day). Lists (`search`, `category`, `brand`, `clearance`) return
the first 24 results with AutoZone's `total` and no paging: narrow with one
facet filter (`filters={facets[].facet: value}`), `brand`, `min_price` /
`max_price` or `sort` (`relevance`, `price_asc`, `price_desc`). List items carry
no rating (`product` does).

`search` takes keywords, AutoZone part numbers and other brands' part numbers
(cross-reference); AutoZone runs ranking tests (`ranking_variant`), so totals
and order can differ between two identical calls. `category` with `vehicle`
returns the parts that fit at year / make / model level (names as `vehicles`
lists them); items AutoZone ties to an engine read `fitment.vehicle_fit`
NEEDS_BASE_VEHICLE. `product` adds specifications, features, safety data
sheets, the deal label and the rating distribution; it carries no per-vehicle
fit list. `reviews` (us) are 10 a page at full depth, sorts `default`,
`most_recent`, `most_helpful`, a `stars` filter, AutoZone's review summary on
page 1 and the reviewer's vehicle as written; no reviewer identity is returned.
`stores` walks the directory (states, then cities, then a city's stores) and
`store` reads one store by slug; there is no stores-near-a-ZIP search.
`store_stock` is Brazil only: one product at a Brazilian store you choose with
its in-store quantity; Brazil `search` and `product` are priced for store 7602
Sao Paulo (Interlagos). Not available: results past the first 24, stores near
a ZIP, stock at a chosen US or Mexican store, search suggestions, VIN lookup,
engine-level fitment, repair guides, AutoZonePro / commercial pricing, Mexico
prices, price history (poll and store the answers), checkout. Failed calls and
refused inputs are not charged; a not-found (an unknown item id, vehicle,
brand, state, city or store) is charged.

### 66. Grocery -- Instacart prices by store at a ZIP, price compare, delivery vs in-store

Instacart (instacart.com), the US and Canada grocery delivery and pickup
marketplace, plus instacart.ca. Namespace `instacart`, 11 endpoints:
`retailers`, `search`, `cross_search`, `product`, `price_compare`,
`categories`, `category`, `deals`, `stores`, `suggestions`, `reviews`. 1
credit per call; `search` 3 (2 when the page fits in Instacart's first
answer); `cross_search` 3 for up to 5 stores, 4 for 6 to 10. `country` is us
by default; ca (CAD, `zip` a Canadian postal code) on every method except
`cross_search` and `reviews`, which are us only and take no `country`.
`language="fr"` (Canada) returns French names, aisles and price text as
Instacart shows them in Quebec; `suggestions` are English only. Every method
but `reviews` takes a `zip`. The request timeout is raised to at least 240s
on every endpoint.

```python
from scavio import ScavioClient

client = ScavioClient()
ic = client.instacart

# --- Every store serving a ZIP: the slug is the retailer input of the other methods.
stores = ic.retailers("10001")["data"]
print(stores["count"], stores["no_markups_count"])
for r in stores["retailers"][:5]:
    print(r["slug"], r["name"], r["delivery_eta"], r["no_markups"], r["accepts_ebt"])

# --- One product priced at every store delivering to the ZIP, low to high.
cmp = ic.price_compare("16408559", "10001")["data"]
print(cmp["stores_checked"], cmp["count"])
for p in cmp["prices"][:5]:
    print(p["retailer_name"], p["price"], p["was_price"], p["no_markups"])

# --- One store's search, then the same product's delivery and in-store price.
res = ic.search("yogurt", "jewel-osco", "60540", sort="price_asc", limit=10)["data"]
print(res["priced_for"]["pricing_label"], res["total"])
for it in res["items"][:3]:
    print(it["product_id"], it["name"], it["size"], it["price"], it["unit_price"], it["deal"])
delivery = ic.product("16408559", "10001", retailer="wegmans")["data"]
instore = ic.product("16408559", "10001", retailer="wegmans", service_type="instore")["data"]
print(delivery["priced_for"], delivery["item"], instore["item"])
print(delivery["ingredients"], delivery["warnings"], delivery["key_nutrients"])

# --- One query across up to 10 stores (us), a store's deals, aisles and pickup locations.
cross = ic.cross_search("milk", "10001", max_retailers=3)["data"]
deals = ic.deals("jewel-osco", "60540", limit=10)["data"]["items"]
tree = ic.categories("wegmans", "10001")["data"]["categories"]
produce = ic.category("produce", "wegmans", "10001", limit=10)["data"]["items"]
pickup = ic.stores("jewel-osco", "60540", limit=5)["data"]["stores"]

# --- Suggestions and reviews (us).
sugg = ic.suggestions("eg", "60540", retailer="jewel-osco")["data"]["suggestions"]
reviews = ic.reviews("16408559")["data"]

# --- Canada in French: CAD prices and French names at a Montreal store.
fr = ic.search("lait", "metro", "H2X1Y4", country="ca", language="fr", limit=10)["data"]
print(fr["currency"], fr["priced_for"]["pricing_label"], fr["items"][0]["price_text"])
```

Every price is Instacart's price for that store, ZIP and service type, named
in `priced_for` (`retailer_slug`, `service_type`, `zip` and the retailer's
`pricing_label` as Instacart shows it, e.g. Costco "Prices are higher than
your local warehouse."). Retailers set their Instacart prices, which can be
above their in-store prices, so an Instacart delivery price is not the
store's shelf price; `service_type="instore"` returns Instacart's in-store
prices where it shows them, and `pickup` the pickup price. Items carry
`price`, `price_text`, `was_price` (the regular price next to a sale price),
`discount_percent` (computed by Scavio from the was price), `deal` (Instacart's
offer badge, e.g. Buy 2, get 3 free), `unit_price`, `loyalty_price`, stock as
Instacart reports it and dietary labels. `retailers` marks `no_markups`
(Instacart's "No markups" label: in-store prices online) and EBT per store.

`product_id` is the same at every store, so a search result feeds `product`,
`price_compare` and `reviews` directly. `price_compare` returns Instacart
delivery prices only, with no unit price or stock (`product` gives them per
store). `cross_search` prices up to 10 stores in Instacart's order, up to 20
items each. `product` returns ingredients, warnings / allergens as given and
the key nutrients Instacart lists, not a full nutrition panel. `deals` is the
store's Sales collection (no coupons). `stores` lists pickup locations nearest
first, with 7 days of hours for the 5 nearest. `reviews` (us) are 15 a page
with a syndication `source` and an `incentivized` flag; no reviewer identity
is returned. A ZIP with no Instacart service area answers an empty list and a
note. Not available: delivery and service fees or order minimums as numbers
(Instacart shows them at checkout), coupons, Instacart+ member prices,
account, order or cart data, price history (poll and store the answers),
`cross_search` and `reviews` in Canada, French `suggestions`. For direct
shelf prices see the `kroger`, `costco`, `aldi`, `publix` and `wholefoods`
namespaces. Failed calls and refused inputs are not charged; a not-found (an
unknown ZIP, product id or category, or a store that does not serve the ZIP)
is charged.

### 67. Auto Parts -- O'Reilly Auto Parts part-number cross-reference with prices, store stock

O'Reilly Auto Parts (oreillyauto.com), the US auto parts retailer, plus
O'Reilly's Mexican store directory. Namespace `oreilly`, 14 endpoints:
`search`, `cross_reference`, `product`, `vehicles`, `compatibility`,
`category`, `categories`, `brand`, `store_stock`, `stores`, `store`,
`suggestions`, `rebates`, `deals`. 2 credits per call; `product` by
`line_code` + `part_number` 4 (by link 2); `cross_reference` 2 with
`part_type_id` + `manufacturer`, 4 with one of them or when several
manufacturers use the number, 6 with neither when one manufacturer matches;
`brand` index (no brand) 4; `store_stock` and `stores` by `zip` 4 (by
`latitude` + `longitude`, or the directory, 2); `deals` 4. Only `stores` and
`store` take `country` (us by default, or mx for the Mexican store directory,
in Spanish); every other method is us only and takes no `country`. The request
timeout is raised to at least 240s on every endpoint. Pair it with the
`autozone` namespace for a two-store parts price check on the same part.

```python
from scavio import ScavioClient

client = ScavioClient()
o = client.oreilly

# --- Another brand's part number in, O'Reilly's matching parts out, priced.
xref = o.cross_reference("PH3614", part_type_id="02269", manufacturer="FRAM")["data"]
print(xref["total"], xref["replacing_brands"], xref["priced_for"])
for it in xref["items"][:3]:
    print(it["line_code"], it["part_number"], it["name"], it["price"], it["core_charge"])
# Without manufacturer: when several brands use the number, the answer is the lists to
# choose from (part_types, manufacturers) with no items; send manufacturer next.
first = o.cross_reference("PH3614")["data"]
print(first["part_types"], first["manufacturers"])

# --- Parts that fit one vehicle: resolve the base_vehicle_id, then search with it.
v = o.vehicles(level="resolve", year=2015, make_id=23076, model_id=31549)["data"]["vehicle"]
pads = o.search("brake pads")["data"]
fit = o.search("brake pads", vehicle={"base_vehicle_id": v["base_vehicle_id"]})["data"]
print(pads["total"], fit["total"], fit["vehicle"])
vin = o.vehicles(level="vin", vin="1HGCM82633A004352")["data"]["vehicle"]

# --- One product in full: price, core charge, deals, rebates, rating, 10 most recent reviews.
p = o.product(line_code="BB", part_number="SC1001")["data"]
print(p["priced_for"], p["price"], p["core_charge"], p["rating"], len(p["reviews"]))
print(o.compatibility("BB", "SC1001", make="Ford")["data"]["models"][:2])

# --- Which stores near a ZIP can hand over the part (states, not unit counts).
stock = o.store_stock("SSB", "48PLT", zip="60540")["data"]
for s in stock["stores"][:3]:
    print(s["store_id"], s["distance_miles"], s["availability"])

# --- Stores near a ZIP, the directory (us and mx), one store, rebates and deals.
near = o.stores(zip="77002")["data"]["stores"]
gdl = o.stores(state="jal", city="guadalajara", country="mx")["data"]["stores"]
store = o.store("4973")["data"]
rebates = o.rebates()["data"]["rebates"]
deals = o.deals()["data"]["offers"]
```

Every price is O'Reilly's price for the store O'Reilly assigns to the request,
named in `priced_for` (`store_id`, `address`, `city`, `state`, `zip`).
O'Reilly prices differ by store, so two calls can be priced for different
stores; there is no store or ZIP input for prices. Items carry `price`,
`regular_price`, `sale_price`, `discount_percent` (computed by Scavio from the
regular price when on sale), `core_charge` (the refundable deposit O'Reilly
adds on parts like batteries until the old part is returned; 0 when none),
`warranty`, `fit_notes` for the requested vehicle, deals and availability per
fulfilment option (store pickup with O'Reilly's pickup time, ship to home).
Lists (`search`, `category`, `brand`, `cross_reference`) return 24 a page and
O'Reilly serves 20 pages (`page` 1-20; above 20 is a 400, not charged); sort
`relevance`, `price_desc`, `price_asc`, `best_selling` or `brand`; filter by
`brand`, `availability` (`store_pickup`, `home_delivery`) or up to 4 attribute
facets. List items carry no rating (`product` does).

`vehicle` takes `{"base_vehicle_id": ...}` from `vehicles(level="resolve")`;
O'Reilly pins year, make and model with it, and submodel and engine show in
`fit_notes`. `vehicles(level="vin")` decodes a 17-character VIN to year, make
and model with the submodel and engine ids. On `product`, `vehicle_fit.fits` is
True when O'Reilly gives the part's application for the vehicle and None
otherwise, never False: check fit with a vehicle `search` or `category`, or
`compatibility`. `cross_reference` maps another brand's or an OE part number to
O'Reilly's parts; it can return 0 matches. `product` returns the 10 most recent
reviews (date, title, text, rating; no reviewer identity) with no paging, sort
or star filter. `store_stock` reports availability states (in store now, store
pickup, pickup time), not unit counts. `stores` returns the 25 nearest stores
within 50 miles of a ZIP or a point with hours, holiday adjustments and
services, or walks the directory by state (+ city) on us and mx. Not available:
unit counts in store stock, a chosen store for prices, reviews past the 10 most
recent, Q&A, Mexico prices or catalog, Canada, license-plate lookup, the weekly
ad, repair guides or trouble codes, O'Reilly Pro / First Call Online
commercial pricing, price history (poll and store the answers), checkout.
Failed calls and refused inputs are not charged; a not-found (an unknown
product, VIN, category, brand, state, city or store) is charged.

### 68. Hardware -- Ace Hardware prices by store, units on hand at nearby stores, weekly ad

Ace Hardware (acehardware.com), the US hardware cooperative. Namespace
`acehardware`, 11 endpoints: `search`, `product`, `store_stock`, `store`,
`stores`, `category`, `categories`, `brand`, `deals`, `weekly_ad`,
`paint_colors`. 1 credit per call; `search` 2 (3 when Ace redirects the search
to a category and the list options are applied to it); `product` 2 (with or
without `store`); `store_stock` 1 per 5 stores (1 store 1, 25 stores 5,
`nearby` 6); `stores` with `details` 1 lookup per store (25 stores 6). An
occasional call costs 2 instead of 1; `credits_used` in the response is what
was charged. US only, so no method takes `country`. The request timeout is
raised to at least 240s on every endpoint. Pair it with the `homedepot` and
`lowes` namespaces for a local hardware price check on the same item (brand +
model).

```python
from scavio import ScavioClient

client = ScavioClient()
ace = client.acehardware

# --- The same item priced for three Ace stores (store numbers are 5-digit strings).
for store in ("10665", "18250", "03085"):
    p = ace.product("72779", store=store)["data"]
    print(store, p["priced_for"], p["price"], p["msrp"])
# Without a store, priced_for names the price list Ace used (CORP is Ace's online price).
print(ace.product("72779")["data"]["priced_for"])

# --- Exact units on hand at chosen stores, or at one store and its 25 nearest.
stock = ace.store_stock("72779", stores=["18250", "17309"])["data"]
for s in stock["stores"]:
    print(s["store_id"], s["units_in_stock"], s["location_code"], s["distribution_center"])
nearby = ace.store_stock("72779", store="18250", nearby=True)["data"]  # 6 credits
print(nearby["count"], nearby["in_stock_count"], nearby["total_units"])

# --- One store, the stores nearest it, and its weekly ad.
store = ace.store("18250")["data"]
print(store["name"], store["address"], store["features"], store["nearest_stores"][:3])
near = ace.stores("03085", details=True, limit=4)["data"]["stores"]
ad = ace.weekly_ad("18250")["data"]
print(ad["title"], ad["valid_from"], ad["valid_to"], ad["total_pages"])
for it in ad["items"][:3]:
    print(it["heading"], it["title"], it["price_text"], it["item_numbers"])
page2 = ace.weekly_ad("18250", page=2, ad_group=ad["ad_group"])["data"]

# --- Lists: search, a category, a brand, deals (listing prices, not a store's price).
hits = ace.search("brass hose nozzle")["data"]
drills = ace.category("/departments/tools/power-tools/cordless-drills", sort="price_asc")["data"]
weber = ace.brand("weber")["data"]
deals = ace.deals(offer="sale")["data"]
print(hits["total"], drills["total"], weber["total"], [p["code"] for p in deals["promotions"]])
tree = ace.categories()["data"]["categories"]
pinks = ace.paint_colors(query="pink")["data"]["colors"]
print([(c["name"], c["brand"], c["hex"]) for c in pinks[:3]])
```

Ace stores are independently owned and operated, and the same item can be
priced differently at different stores (Ace's terms: pricing varies by
location). `product` with `store` returns the price as Ace shows it for that
store, with `priced_for` {`store_id`, `price_list`}; without a store,
`priced_for` names the price list Ace used (`CORP` is Ace's online price).
Captured 2026-11-23: item 72779 (Ace ice melt, 40 lb) at $35.99 for store
10665 (New York), $21.99 for 18250 (Chicago) and $18.99 for 03085 (Kalona,
Iowa). `msrp` is reported as Ace gives it and can be below a store's price.
Listing prices (`search`, `category`, `brand`, `deals`) are the price Ace shows
in its listing (`price_list` per item), not a store's price; for a store's
price call `product` with `store`. Lists return 15, 30 (default), 50, 100 or
200 a page, sorted `relevance`, `price_asc`, `price_desc`, `name_asc`,
`name_desc`, `newest` or `oldest`, filtered by `brand`, `offer` (`sale`,
`ace_rewards`, `buy_and_get`, `buy_more_save`), `on_sale` or facet `filters`.

Store numbers are 5 digits with leading zeros kept (`"03085"`), shown in every
Ace store page link (acehardware.com/store-details/<number>); there is no store
search by ZIP or city, and `stores` lists the 25 stores Ace names as nearest to
one store. `store_stock` returns exact units on hand as Ace reports them
(`units_in_stock`, `soft_units`, the shelf `location_code` and the regional
distribution centre's units); Ace answers 0 for a store number or product it
does not know, exactly as for one out of stock. `weekly_ad` returns one store's
circular with `valid_from` / `valid_to` and items with the ad's own price text.
`deals` adds Ace's site-wide promotions with codes and start / end dates.
`paint_colors` lists about 5,300 colours (Benjamin Moore, Clark+Kensington,
Magnolia Home) with hex and RGB. Not available: review or Q&A text (rating and
count only), search suggestions, ZIP or city store search, pickup or delivery
dates, price history (poll and store the answers), Ace Rewards member prices,
Ace Handyman, rentals, Ace-licensed stores outside the US, checkout. Failed
calls and refused inputs are not charged; a not-found (an unknown product,
category, brand or store) is charged.

### 69. Farm and Ranch -- Tractor Supply prices by store and price zone, store stock, fulfilment

Tractor Supply (tractorsupply.com), the US rural lifestyle retailer. Namespace
`tractorsupply`, 12 endpoints: `search`, `product`, `store_prices`,
`store_stock`, `fulfillment`, `stores`, `store`, `category`, `categories`,
`brand`, `deals`, `promotions`. 1 credit per call; `product` 2 on the first
call for a store not yet looked up; `store_prices` 1 per 5 lookups (each
store's price, a store's details when not yet known, the item: 25 new stores
cost 11). `credits_used` in the response is what was charged. US only, so no
method takes `country`. The request timeout is raised to at least 240s on
every endpoint. Pair it with the `acehardware`, `walmart` and `chewy`
namespaces for a price check on the same item.

```python
from scavio import ScavioClient

client = ScavioClient()
tsc = client.tractorsupply

# --- The same bag of feed priced for two stores (store or zip is required).
for store in ("1933", "1923"):
    p = tsc.product("2340147", store=store)["data"]
    print(store, p["priced_for"]["zone"], p["price"], p["mapp"])

# --- One item at up to 25 stores in one call, or at the stores nearest a ZIP.
sp = tsc.store_prices("2340147", stores=["1933", "1923"])["data"]
print(sp["price_range"])
for s in sp["stores"]:
    print(s["store_id"], s["city"], s["state"], s["zone"], s["price"])

# --- Exact units per store, with stock in transit and its pickup date.
stock = tsc.store_stock("2340147", zip="59301")["data"]
print(stock["count"], stock["in_stock_count"], stock["total_units"], stock["in_transit_units"])
for s in stock["stores"]:
    print(s["store_id"], s["distance_miles"], s["units"], s["status"], s["in_transit"])

# --- Pickup and delivery options for one item at one store and a ZIP.
f = tsc.fulfillment("2340147", "1933", "59330")["data"]
print(f["pickup"], [(o["type"], o["delivery_date"]) for o in f["delivery_options"]])

# --- Stores near a ZIP, one store, an item's promotions.
for s in tsc.stores("59301")["data"]["stores"]:
    print(s["store_id"], s["name"], s["zone"], s["services"][:3])
print(tsc.store("1933")["data"]["hours_text"])
for promo in tsc.promotions("3609112")["data"]["promotions"]:
    print(promo["name"], promo["starts"], promo["ends"])

# --- Lists priced for one store: search, a category, a brand, deals.
hits = tsc.search("layer pellets", store="1933")["data"]
feed = tsc.category("/tsc/catalog/poultry-feed", store="1933", sort="price_asc")["data"]
brand = tsc.brand("Producer's Pride", store="1933")["data"]
sale = tsc.deals(store="1933")["data"]
print(hits["total"], feed["total"], brand["total"], sale["total"])
tree = tsc.categories()["data"]["categories"]
```

Tractor Supply prices by store, so `search`, `product`, `category`, `brand` and
`deals` need `store` (a Tractor Supply store number) or `zip` (the nearest
store Tractor Supply lists for it is used); there is no default store. Every
price answer carries `priced_for` {`store_id`, `zone`, `city`, `state`, `from`,
`zip`}. Tractor Supply's terms note that prices may vary in different
geographic markets, and the same item can be priced differently at different
stores. Captured 2026-11-24: Producer's Pride 16% Layer Pellets, 50 lb (item
2340147) at $14.49 for store 1933 (Glendive, MT, zone 81) and $20.19 for store
1923 (Port Orchard, WA, zone 92). Some items carry a manufacturer's minimum
advertised price (`mapp`) and show one price everywhere. Item numbers are 7
digits (`items[].item_number`) and are the input of `product`, `store_prices`,
`store_stock`, `fulfillment` and `promotions`. Lists return 24 (default), 48,
96 or 200 a page, pages 1-100, sorted `popular`, `rating`, `name_asc`,
`name_desc`, `price_asc`, `price_desc`, `recent` or `new_arrivals`, filtered
by `brand`, `on_sale`, `new`, `pickup`, `rating` or facet `filters`.

`store_stock` returns units as Tractor Supply reports them (not a promise),
the status and in-transit units with the pickup date Tractor Supply gives.
`fulfillment` returns pickup units and the delivery options (standard, same
day, ship to store) with delivery dates and order cut-offs. `stores` lists the
stores nearest a ZIP with address, hours, price zone, services (propane,
trailer rental, PetVet, pet wash, ...) and dated store events. `promotions`
lists an item's promotions with start and end dates. Not available: review or
Q&A text (rating and count only), search suggestions, the weekly ad, a
clearance list, price history (poll and store the answers), Neighbor's Club
member prices, live chick availability, Petsense, checkout. Failed calls and
refused inputs are not charged; a not-found (an unknown item, category, brand,
store or a ZIP with no store) is charged.

### 70. Arts and Crafts -- Michaels store stock near a ZIP, prices with Reg. labels, variants

Michaels (michaels.com), the US and Canada arts and crafts retailer. Namespace
`michaels`, 11 endpoints: `search`, `product`, `store_stock`,
`store_inventory`, `stores`, `store`, `category`, `categories`, `brand`,
`deals`, `suggestions`. 2 credits per call; `category` and `deals` 4 when the
category is a `/shop/` link or path (one more call finds its code path; a code
path costs 2). `credits_used` in the response is what was charged. `country`
is `"us"` (default, www.michaels.com, USD) or `"ca"` (canada.michaels.com,
CAD); `language` is `"en"` (default) or `"fr"` (with `"ca"` only). `stores`,
`categories` and `suggestions` are US only and take no `country`. The request
timeout is raised to at least 240s on every endpoint. Pair it with the
`walmart` and `amazon` namespaces (and the
[Etsy API](https://scavio.dev/etsy-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme))
for a price check on the same item.

```python
from scavio import ScavioClient

client = ScavioClient()
mi = client.michaels

# --- One skein's units at the Michaels stores near a ZIP, as Michaels reports them.
stock = mi.store_stock("10228177", "10001")["data"]
print(stock["count"], stock["in_stock_count"], stock["total_units"])
for s in stock["stores"]:
    print(s["store_id"], s["name"], s["distance_miles"], s["units"], s["pickup_text"], s["virtual"])

# --- Up to 30 SKUs at one store.
inv = mi.store_inventory("1191", ["10228177", "10816737"])["data"]
print([(i["sku"], i["units"]) for i in inv["items"]], inv["not_reported"])

# --- A product: price next to Michaels' own Reg. label, promotions with their dates,
#     every colour with its price and UPC, online stock (not a store's), Pro-pack price.
p = mi.product("10228177")["data"]
print(p["price"], p["was_price_text"], p["online_stock"], p["pro_pack"])
for promo in p["promotions"]:
    print(promo["text"], promo["starts"], promo["ends"])
for v in p["variants"][:5]:
    print(v["sku"], v["options"], v["price"], v["was_price"], v["upc"])

# --- The same item in Canada (CAD), in English or French.
ca = mi.product("10816737", country="ca")["data"]
print(ca["market"]["currency"], ca["price"], ca["was_price_text"])

# --- Lists: search, a category, a brand, deals (Sale, New, Clearance, Great Buy).
hits = mi.search("yarn", sort="price_asc", on_sale=True)["data"]
for it in hits["items"][:5]:
    print(it["sku"], it["name"], it["price"], it["was_price_text"], it["seller_type"])
canvas = mi.category("/shop/art-supplies/artist-canvas")["data"]
cricut = mi.brand("Cricut")["data"]
xmas = mi.deals(query="christmas")["data"]
print(hits["total"], canvas["total"], cricut["total"], xmas["total"])

# --- Stores near a ZIP (US), one store, departments, suggestions.
for s in mi.stores("60657")["data"]["stores"][:3]:
    print(s["store_id"], s["name"], s["distance_miles"], s["services"])
print(mi.store("1040")["data"]["hours_text"])
tree = mi.categories()["data"]["categories"]
print([t["term"] for t in mi.suggestions("yarn")["data"]["suggestions"]])
```

Prices are national per country: the store does not change them, it matters
for stock. Captured 2026-11-24: Cricut Explore 5 in Teal & Essential Bundle
(SKU 10816737) at $199.00 next to Michaels' "Reg.$249.00" on www.michaels.com
and CAD 269.99 next to "Reg.$349.99" on canada.michaels.com. `was_price_text`
keeps Michaels' own label and `discount_percent` is arithmetic on the two
prices. `promotions` carry Michaels' own offer text with its start and end
dates, as given. `store_stock` returns units as Michaels reports them for
pickup, not a promise (Soft Classic Solid Yarn by Loops & Threads, SKU
10228177: 85 units at store 1191, New York); virtual or pop-up stores appear
with 0 units and `virtual: true`. `online_stock` on a product is Michaels'
online stock, not a store's. Search and the list methods mix Michaels items
and Marketplace items (`seller_type`); Marketplace items carry a seller id, no
seller name. A UPC search answers with the product group's lead SKU. With
`country="ca"` a category is a code path (search facets list them). Lists
return up to 100 a page (default 40), sorted `best_match`, `best_sellers`,
`new_arrivals`, `price_asc`, `price_desc` or `rating`, filtered by `brand`,
price, rating, store pickup, same-day, ship to me, sale, new, clearance, great
buy, `seller` or facet `filters` ({key: [values]}). Not available: review or
Q&A text (rating and count only), the weekly ad, coupons, classes and events,
aisle locations, Marketplace seller names, custom framing, price history (poll
and store the answers), checkout. Failed calls and refused inputs are not
charged; a not-found (an unknown product, category, brand or store) is charged.

### 71. Sneakers and Sportswear -- Nike sale prices, sizes with GTIN, release calendar

Nike (nike.com, including Jordan Brand). Namespace `nike`, 8 endpoints:
`search`, `product`, `category`, `brand`, `deals`, `releases`, `release`,
`reviews`. 1 credit per call; `credits_used` in the response is what was
charged. `country` is a two-letter storefront code (default `"us"`,
www.nike.com; 62 storefronts in 42 countries, `"cn"` is www.nike.com.cn) and
`language` picks the storefront language where a country has several (`ch`:
de, en, fr, it; `be`: nl, de, en, fr; `ca`: en, fr; `us`: en, es; `jp`: ja,
en). `releases` and `release` are not offered on `vn`, `cn` or `jp` in
English; `reviews` is not offered on `cn`. The request timeout is raised to at
least 240s on every endpoint. Nike has no public API for catalog, prices or
launches. Pair it with the `footlocker`, `dicks`, `amazon` and `ebay`
namespaces for a price check on the same style code.

```python
from scavio import ScavioClient

client = ScavioClient()
nk = client.nike

# --- One product: price next to Nike's full price and discount percent as Nike gives them,
#     every size with its GTIN and Nike's status (sizes, not stock levels), colorways.
p = nk.product("DD1503-103")["data"]
print(p["name"], p["price"], p["full_price"], p["discount_percent"], p["currency"], p["status"])
for s in p["sizes"][:5]:
    print(s["label"], s["localized_label"], s["gtin"], s["status"])
for c in p["colorways"][:3]:
    print(c["style_color"], c["color"], c["price"], c["full_price"])

# --- The same style color on other storefronts, each in its own currency.
for country in ("gb", "fr", "jp"):
    hits = nk.search("DD1503-103", country=country)["data"]
    print(country, [(i["style_color"], i["price"], i["currency"]) for i in hits["items"][:1]])

# --- Lists: search, a listing, Jordan / ACG / SB, the Sale listing (first page only: 24 groups).
hits = nk.search("dunk low", sort="price_low")["data"]
for it in hits["items"][:5]:
    print(it["style_color"], it["name"], it["price"], it["full_price"], it["promotions"])
token = hits["facets"][0]["options"][0]["filter"]
narrowed = nk.search("dunk low", filter=token)["data"]
mens = nk.category("mens-shoes-nik1zy7ok")["data"]
jordan = nk.brand("jordan")["data"]
sale = nk.deals(gender="women")["data"]
print(hits["total"], narrowed["total"], mens["total"], jordan["total"], sale["total"])

# --- The launch calendar: price, release start, method and a per-size level for launch items.
cal = nk.releases()["data"]
for l in cal["launches"][:3]:
    print(l["style_color"], l["name"], l["price"], l["release_start"], l["method"])
    print([(s["size"], s["level"], s["available"]) for s in l["sizes"][:4]])
bred = nk.release("IX8180-001")["data"]
print(bred["thread"]["title"], bred["count"])

# --- A review summary: totals, averages, Nike's own summary and the 3 newest reviews.
r = nk.reviews("CW2288-111")["data"]
print(r["total_reviews"], r["average_rating"], r["average_size_rating"], r["review_summary"])
```

Prices are per storefront and differ between markets, also inside the euro
zone. Captured 2026-11-24: the Nike Dunk Low (style color DD1503-103) at
$78.97 next to a $120 full price (34%) on www.nike.com, £54.99 next to £109.99
(50%) on nike.com/gb, €59.99 next to €119.99 (50%) on nike.com/fr and ¥17,050
on nike.com/jp. `price`, `full_price` and `discount_percent` are as Nike gives
them; `promotions` carry Nike's offer text with its start and end dates (UTC),
as given. Search and the list methods return Nike's first page only (the 24
product groups Nike's page shows first; `total` and `total_pages` as Nike
gives them); `search` takes one facet token in `filter` (a token from a
filtered answer already carries the filters applied there), the list methods
up to 6. Product sizes carry a GTIN and Nike's status, not a stock level.
Launch items carry `method` (LINE or DRAW, as Nike labels it) and a per-size
`level` (HIGH, MEDIUM, LOW or OOS as Nike gives it); before a launch Nike can
show LOW on every size. Read-only data: no entry or purchase. Reviews are the
summary and the 3 newest reviews, no paging and no reviewer names. Not
available: store locator, in-store or pickup stock, stock levels for regular
products, review paging or Q&A, search suggestions, pages past the first,
member prices, gift cards, Nike Factory store prices, Converse, checkout.
Failed calls and refused inputs are not charged; a not-found (an unknown
product, listing or launch) is charged.

### 72. Office Supplies -- Staples ink and paper prices, price per unit, store stock near a ZIP

Staples (staples.com, the US office supply retailer; Staples Canada at
staples.ca). Namespace `staples`, 12 endpoints: `search`, `product`,
`category`, `categories`, `deals`, `coupons`, `store_stock`, `stores`,
`store`, `reviews`, `questions`, `trending`. 1 credit per call;
`credits_used` in the response is what was charged. `country` is `"us"`
(default, www.staples.com, USD) or `"ca"` (www.staples.ca, Staples Canada,
CAD) and `language` is `"en"` (default) or `"fr"` (with `"ca"` only), on
`search` and `product`; every other method is US only (no `country`). The
request timeout is raised to at least 240s on every endpoint. Staples has no
public API for its catalog, prices or store stock (Staples Business Advantage
connects contract buyers' purchasing systems). Pair it with the `amazon`,
`walmart`, `target` and `bestbuy` namespaces for a price check on the same
item.

```python
from scavio import ScavioClient

client = ScavioClient()
st = client.staples

# --- Search: 40 a page, Staples' own price per unit ($5.00/Ream, $0.10 Cost Per Page).
hits = st.search("copy paper", sort="price_low")["data"]
print(hits["total"], hits["total_pages"])
for it in hits["items"][:5]:
    print(it["item_id"], it["name"], it["price"], it["was_price"], it["price_per_unit_text"])
token = hits["facets"][0]["values"][0]["filter"]
narrowed = st.search("copy paper", filters=[token], brand="Hammermill")["data"]

# --- One product: price per unit, pack size, page yield, Staples' promotion texts with their
#     expiry, coupon codes, plus delivery dates for a ZIP and pickup units at one store.
p = st.product("122374", zip="60540", store="1633")["data"]
print(p["name"], p["price"], p["was_price"], p["price_per_unit"], p["price_per_unit_unit"])
print(p["pack_size"], p["page_yield"], p["offer_expires"], [x["text"] for x in p["promotions"]])
print(p["availability"]["pickup"], [(o["mode"], o["date_text"]) for o in p["availability"]["options"]])

# --- Units of one item at the stores near a ZIP that have it for pickup, as Staples reports them.
ss = st.store_stock("2724258", "60540")["data"]
print(ss["name"], ss["count"], ss["total_units"])
for s in ss["stores"]:
    print(s["store_number"], s["address"]["city"], s["distance_miles"], s["units"], s["pickup_text"])

# --- Canada: Staples Canada's top matches and its products, in English or French (CAD).
ca = st.search("hp 67", country="ca")["data"]
for it in ca["items"]:
    print(it["item_id"], it["handle"], it["name"], it["price"], it["currency"])
cp = st.product(handle=ca["items"][0]["handle"], country="ca")["data"]
print(cp["name"], cp["price"], cp["currency"], cp["barcode"])

# --- Reviews (up to 100 a page) and customer questions with their answers.
rv = st.reviews("24430099", limit=100, sort="newest")["data"]
print(rv["total"], rv["rating"], rv["review_summary"])
for r in rv["reviews"][:3]:
    print(r["rating"], r["title"], r["verified_purchase"], r["incentivized"])
qa = st.questions("990119", sort="most_answered")["data"]
for q in qa["questions"][:3]:
    print(q["text"], [a["text"] for a in q["answers"][:1]])

# --- Deals, coupons, stores, categories, trending.
deals = st.deals(query="laptop")["data"]
coupons = st.coupons()["data"]
print([(c["code"], c["headline"], c["ends"]) for c in coupons["coupons"][:3]])
stores = st.stores(city="Chicago, IL")["data"]
paper = st.categories(category="SC1676")["data"]
listing = st.category("CL140691", sort="rating")["data"]
print(deals["total"], stores["count"], paper["count"], listing["total"], st.trending()["data"]["terms"])
```

Prices are national: the ZIP changes delivery availability and dates, the
store changes pickup units, neither changes the price. Captured 2026-11-24:
Hammermill Copy Plus (item 122374, 10 reams) at $49.99 next to Staples'
Regular $83.19, at "$5.00/Ream", with "Offer Expires on 11/28/2026"; the HP
64XL Black High Yield cartridge (item 2724258, "Prints Up to 600 Pages") at
Staples' own "$0.10 Cost Per Page", in stock at 7 stores near ZIP 60540 with
63 units in all (12 at store 1633, Naperville, "Ready in 30 mins"). `price`
and `was_price` are as Staples shows them (`was_price` is Staples' Regular
price, given only when above the price); `discount_percent` is computed by
Scavio from the two. `store_stock` lists only the stores that have the item;
an empty list means no nearby store has it or it is not offered for store
pickup. Staples returns a `threshold` value beside the units; it is passed
through as given. staples.com publishes no UPC (`model` is the manufacturer
part number); Staples Canada products carry a `barcode`. Canada search returns
Staples Canada's top matches (about 5, no paging, sort or filters). Reviews
carry no reviewer names and are pooled across an item's sizes and packs. Not
available: the weekly ad, search suggestions, print and tech service prices,
ink recycling rewards, Rewards member prices, price match requests, Staples
Business Advantage contract prices, price history (poll and store the
answers), checkout. Failed calls and refused inputs are not charged; a
not-found (an unknown item, class, department or store) is charged.

### 73. Dollar Stores -- Dollar Tree case prices, unit prices, store stock

Dollar Tree (dollartree.com, the US and Canada discount variety store
chain). Namespace `dollartree`, 10 endpoints: `search`, `product`,
`category`, `categories`, `brand`, `deals`, `store_stock`, `stores`, `store`,
`reviews`. 1 credit per call, `stores` 5; `credits_used` in the response is
what was charged. Every method is US only (www.dollartree.com, USD; no
`country`) except `store`, which also takes `country="ca"` (Dollar Tree
Canada store pages, English, no prices): Dollar Tree Canada has no shopping
site. The request timeout is raised to at least 240s, and to 300s on
`store_stock`, `stores` and `reviews`. Dollar Tree has no public API for its
catalog, prices or store stock (suppliers work through its vendor portal and
EDI). Pair it with the `dollar_general`, `walmart`, `target` and `instacart`
namespaces for a price check on the same item.

```python
from scavio import ScavioClient

client = ScavioClient()
dt = client.dollartree

# --- Search: 48 a page, unit price next to Dollar Tree's own case price and case pack.
hits = dt.search("paper plates", sort="price_low")["data"]
print(hits["total"], hits["total_pages"])
for it in hits["items"][:5]:
    print(it["item_id"], it["name"], it["price"], it["case_price"], it["case_pack"], it["minimum_quantity"])
facet_id = hits["facets"][0]["values"][0]["id"]
narrowed = dt.search("paper plates", filters=[facet_id], price_point=1.25)["data"]

# --- One item: unit price, case price, case pack, minimum order, split-case rules, online stock.
p = dt.product("221159")["data"]
print(p["name"], p["price"], p["case_price"], p["case_pack"], p["minimum_quantity"], p["split_case"])
print(p["banner_code"], p["split_case_fee"])  # raw Dollar Tree fields, as given
print(p["online_stock"], p["upcs"][:3])

# --- Units at one store plus its nearby stores (store number required; slow: tens of seconds).
near = dt.stores("60540")["data"]  # 5 credits
store_number = near["stores"][0]["store_number"]
ss = dt.store_stock("221159", store_number)["data"]
print(ss["store"]["units"], ss["nearby_in_stock"], len(ss["nearby_stores"]))
home = ss["ship_to_home"]  # max_order_units: the most units orderable for delivery, not cases x case_size
print(home["dc_number"], home["cases"], home["max_order_units"], home["eta"], ss["ship_to_store"]["eta"])

# --- Store pages (US, or Canada with country="ca"), with hours and services.
s = dt.store(slug="ny/new-york/2182-3rd-avenue")["data"]
print(s["store_number"], s["address"]["city"], s["accepts_ebt"], s["more_choices"])
ca = dt.store(slug="on/toronto/2340-eglinton-ave-west", country="ca")["data"]

# --- Newest reviews (up to about 98 per call), with syndication flags.
rv = dt.reviews("206652")["data"]
print(rv["rating"], rv["review_count"], rv["count"])
for r in rv["reviews"][:3]:
    print(r["rating"], r["title"], r["syndicated"], r["syndication_source"])

# --- Categories, a category listing, a brand, and the deal listings.
tree = dt.categories()["data"]
listing = dt.category("3804024826", sort="price_low")["data"]
dixie = dt.brand("Dixie")["data"]
more = dt.deals(type="more_choices")["data"]
print(tree["total_categories"], listing["total"], dixie["total"], more["total"])
```

Prices are Dollar Tree's online unit prices from one national online price
list (the same at every store and ZIP measured); Dollar Tree notes that prices
and availability may vary between stores and online, and in-store shelf
prices are not published online. Online orders are by the case. Captured
2026-11-24: item 221159 (9-in. White Paper Plates, 40-ct. Packs) at $1.50 a
unit, `case_pack` 30, `case_price` $45.00, `minimum_quantity` 5; item 380886
(Heavy-Duty 10-in Ultra Paper Plates, 10-pc Pack) at $1.50 a unit, 24 to a
case, $36.00 a case. A case pack or case price Dollar Tree gives as 0 is
`None`, never computed; stores sell single units. `split_case.available` is
computed by Scavio as `minimum_quantity < case_pack` (Dollar Tree's own flag
reads N on every item); on `product`, `split_case_fee` is Dollar Tree's raw
field as given (its meaning is not published, so it is not a fee) and
`banner_code` is Dollar Tree's banner code (DT or FD), not a store-brand flag.
`store_stock` needs a store number (a ZIP alone does not pick a store): item
221159 showed 116 units at store 5126 (New York) and 63 nearby stores, 59 of
them with stock; `ship_to_home` came from distribution centre 99006 with 2,374
cases of 30 and `max_order_units` 75,570 (the most units orderable for
delivery, the same at every store). `store.status` can be `None`, and some
rural stores list no nearby stores.
`store_stock`, `stores` and `reviews` are slow (usually 10-35 s, up to about
2.5 minutes). Search matches item numbers, not UPCs. Reviews are the newest
only (no other sort, no star filter, no Q&A, no reviewer names); many are
syndicated from brand sites and flagged. More Choices is Dollar Tree's
multi-price assortment. Not available: search suggestions, the weekly ad,
deal validity dates, Quick Order / bulk ordering, gift cards, Canada products
and prices, price history (poll and store the answers), checkout. Failed calls
and refused inputs are not charged; a not-found (an unknown item, category,
brand or store) is charged.

### 74. Tires -- Discount Tire tire prices by store, vehicle fitment, store stock

Discount Tire (discounttire.com, the US tire and wheel retailer, America's
Tire in parts of CA, PA, NJ and NY). Namespace `discounttire`, 15 endpoints:
`search`, `vehicle`, `vehicle_tires`, `product`, `model`, `store_stock`,
`stores`, `store`, `reviews`, `store_reviews`, `wheels`, `browse`,
`categories`, `suggestions`, `appointments`. 1 credit per call;
`credits_used` in the response is what was charged. Every method is US only
(www.discounttire.com, USD; no `country`): Discount Tire and America's Tire
are one catalog. The request timeout is raised to at least 240s. Discount
Tire has no public product API (it runs an affiliate programme through CJ,
and fleet customers use an account portal). Pair it with the `walmart`,
`sams_club` and `amazon` namespaces for the same tire (match on
manufacturer part number or GTIN), and with `autozone` and `oreilly` for
parts. See the [Discount Tire API page](https://scavio.dev/discounttire-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
dt = client.discounttire

# --- Tires in one size at one store: price per tire, promotions with end dates, units there.
hits = dt.search("225/65R17", store="1009", sort="price_low")["data"]
print(hits["store"]["name"], hits["total"])
for it in hits["items"][:5]:
    print(it["item_number"], it["name"], it["price"], (it["stock"] or {}).get("units"), it["promotions"])
# No set-of-four price field: 4 x price is arithmetic, label it as such.
print("4 tires (arithmetic):", 4 * hits["items"][0]["price"])

# --- The same tire at another store, chosen by ZIP (the nearest store is used and echoed).
p = dt.product("108547", zip="85251")["data"]
print(p["store"]["store_code"], p["store"]["brand"], p["price"], p["gtin"], p["manufacturer_part_number"])
print(p["tire"]["load_index_speed"], p["tire"]["utqg"], p["tire"]["tread_depth"])

# --- Vehicle fitment, one step per call: years -> makes -> models -> trims -> size options -> fitment.
makes = dt.vehicle(year=2022)["data"]["options"]
models = dt.vehicle(year=2022, make="Ford")["data"]["options"]        # [{vehicle_id, model}]
trims = dt.vehicle(vehicle_id="17361")["data"]["options"]             # [{trim_id, trim}]
sizes = dt.vehicle(vehicle_id="17361", trim_id="52455")["data"]["options"]  # [{assembly_id, ...}]
fit = dt.vehicle(vehicle_id="17361", trim_id="52455", assembly_id="0000E28B")["data"]["fitment"]
print(fit["front_size"], fit["rear_size"], fit["staggered"], fit["optional_sizes"][:1])

# --- Tires that fit the vehicle at one store, original equipment flagged.
vt = dt.vehicle_tires("17361", "52455", "0000E28B", store="1009")["data"]
print(vt["total"], [i["name"] for i in vt["items"] if i["original_equipment"]])
# Staggered vehicles come back as front / rear sets, each tire with its own price.
sets = dt.vehicle_tires("16990", "51166", "0000DI40", store="1009")["data"]
first = sets["items"][0]
print(first["front"]["price"], first["rear"]["price"], first["price_note"])
# Treadwell ranking: Discount Tire's own estimates, as given.
tw = dt.vehicle_tires("17361", "52455", "0000E28B", store="1009", ranking="treadwell")["data"]

# --- Exact units at the stores near a ZIP (5 stores per page).
ss = dt.store_stock("108547", "85251", radius=25)["data"]
for s in ss["stores"]:
    print(s["store_code"], s["distance_miles"], s["stock"][0]["units"], s["stock"][0]["message"])

# --- Every size of a model, wheels, browse, categories, suggestions.
m = dt.model("michelin-defender-2", store="1009")["data"]
print(m["item_count"], m["price_range"])
wheels = dt.wheels(diameter=20, width=9, bolt_pattern="6-135", store="1009")["data"]
allseason = dt.browse(category="all-season-tires", store="1009")["data"]
cats = dt.categories()["data"]
sugg = dt.suggestions("michelin")["data"]

# --- Stores, one store, reviews, and the read-only appointment calendar.
stores = dt.stores("85251")["data"]
store = dt.store("1009")["data"]
print(store["brand"], store["hours"][:2])
rv = dt.reviews("108547", sort="most_helpful")["data"]
print(rv["rating"], rv["review_count"], rv["total_pages"])
srv = dt.store_reviews("1009")["data"]
cal = dt.appointments("1009")["data"]
print([(d["date"], d["bookable"], d["slot_count"]) for d in cal["days"]])
```

Prices, stock and promotions are per store: `search`, `vehicle_tires`,
`product`, `model`, `wheels` and `browse` take `store` (a store code from
`stores`) or `zip` (the nearest store is used), and every answer names the
store used in `store`. Price can differ between stores and is not different
at every store: measured 2026-11-25, Michelin Defender 2 225/65R17 (item
108547) was $206 a tire at 9 stores in 8 states and $205 at an America's Tire
store in New Jersey; across 45 tires, the stores measured in Texas, Florida
and Washington showed no differences, a California store 1, a Michigan store
3 and the New Jersey store 13 of 32. `price` is per tire or wheel: Discount
Tire publishes no set-of-four price. Promotions are Discount Tire's own title
and text with its end date (`ends`, ISO 8601 UTC, and `ends_text` as given);
no start date. Captured 2026-11-25: the 2022 Ford F-150 XLT Crew Cab 2WD
(`vehicle_id` 17361, `trim_id` 52455, `assembly_id` 0000E28B) runs 245/70R17
and had 157 tires at store 1009; the 2022 Corvette Stingray (245/35R19 front,
305/30R20 rear) had 93 front / rear sets (a set is 2 front + 2 rear).
Treadwell ranking fields are Discount Tire's own estimates, as given. Store
stock is the exact unit count per store; a store with 0 units can still say
"Available as soon as <date>". Reviews are Discount Tire's own, fully paged,
with no reviewer names. Appointments are read only: Scavio never books; slot
`start` and `end` are the store's local time (YYYY-MM-DDTHH:MM, no time
zone). Not available: the deals page text, road hazard and certificate prices,
financing, installation and fee amounts, the Treadwell chat, fleet accounts,
Tire Rack, price history (poll and store the answers), checkout and booking.
Failed calls and refused inputs are not charged; a not-found (an unknown
item, model, category, brand or store) is charged.

### 75. Tools and equipment -- Vevor prices per storefront, deals, shipping by state

VEVOR (vevor.com, the tools and equipment seller with storefronts in 13
countries). Namespace `vevor`, 11 endpoints: `search`, `product`, `shipping`,
`reviews`, `questions`, `suggestions`, `categories`, `category`,
`collections`, `deals`, `prices`. 1 credit per call, `prices` 3;
`credits_used` in the response is what was charged. Every method except
`prices` takes `country` (default `us`) and `language` (default the
storefront's first); `prices` takes `sku` only and asks every storefront. The
request timeout is raised to at least 240s. VEVOR has no public product API
(it runs an affiliate programme through Awin and other networks; the Pro
Member, Dealer & Distributor and dropshipping programmes are sign-up forms,
not APIs). VEVOR also sells on other marketplaces: pair it with the `amazon`,
`walmart`, `home_depot`, `tractorsupply`, `tiktok_shop` and `ebay` namespaces
for the same item (match on model or SKU evidence), and with `harbor_freight`
as an alternative store, not the same item. See the
[Vevor API page](https://scavio.dev/vevor-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
vv = client.vevor

# --- Search in the storefront language: 60 items a page, price, was price during a deal, stock.
hits = vv.search("welder")["data"]
print(hits["market"], hits["total"], hits["has_more"])
for it in hits["items"][:5]:
    print(it["sku"], it["name"], it["price"], it["was_price"], it["currency"], it["deal_ends"], it["stock_units"])
# Each storefront language has its own search index: search de in German.
de = vv.search("schweissgeraet", country="de", sort="price_low", in_stock=True)["data"]

# --- One product: deal window, variants with their own price and stock, specs.
p = vv.product("DHJMIGMMAMIGLL6WNV5")["data"]
print(p["price"], p["was_price"], p["deal"], p["stock_units"])
for v in p["variants"]:
    print(v["sku"], v["attributes"], v["price"], v["stock_units"])

# --- Shipping: the state drives the fee and delivery date in the US (province in Canada).
ship = vv.shipping("DHJMIGMMAMIGLL6WNV5", state="AK", zip="99501")["data"]
print(ship["fee"], ship["currency"], ship["free_shipping"], ship["delivery"])

# --- The same SKU on all 13 storefronts, each in its own currency (3 credits).
pr = vv.prices("GYQXJBMQJQYPKEO1LV0")["data"]
for s in pr["storefronts"]:
    print(s["country"], s["status"], s["price"], s["currency"], s["was_price"], s["stock_units"])

# --- Reviews (one pool shared across storefronts, many languages), questions.
rv = vv.reviews("CKKMJ3300LBSAPPKZV1", page_size=100, sort="newest")["data"]
print(rv["rating"], rv["review_count"], [(r["language"], r["country"]) for r in rv["reviews"][:3]])
qa = vv.questions("DHJMIGMMAMIGLL6WNV5")["data"]

# --- Category tree, one category, Best Sellers, Daily Deals, suggestions.
tree = vv.categories()["data"]
ice = vv.category("40035", sort="price_low")["data"]
print(ice["title"], ice["total"], ice["total_is_lower_bound"])
best = vv.collections(type="best_sellers")["data"]
daily = vv.deals(type="daily_deals")["data"]
sugg = vv.suggestions("ice")["data"]
```

Storefronts (`country`, `language`): `us` (www.vevor.com, USD; en, es), `ca`
(www.vevor.ca, CAD; en, fr), `gb` (www.vevor.co.uk, GBP), `au`
(www.vevor.com.au, AUD), `de`, `fr`, `es`, `it`, `nl` (EUR, each in its own
language), `pl` (PLN), `mx` (MXN, es), `no` (www.vevor.co.no, EUR) and `eu`
(eur.vevor.com, VEVOR's storefront for the other European countries, EUR; en,
sv, da, fi, no, pt, cs, el, sk, hu, ro). The same SKU has its own price on each
storefront: measured 2026-11-25, one SKU (GYQXJBMQJQYPKEO1LV0) was 195.01 USD
on www.vevor.com, 233.90 CAD on www.vevor.ca, 175.90 GBP on www.vevor.co.uk,
170.90 EUR on www.vevor.de, 261.99 EUR on www.vevor.co.no and 721.90 PLN on
www.vevor.pl. Price and stock do not change by ZIP; the shipping fee and
delivery date change by US state (`state`, required for `us`) or Canadian
province (`province`, required for `ca`): a welder to Alaska (AK 99501) had a
$130 fee, contiguous states were measured free. `was_price` is given only while
a VEVOR deal is active (`deal.starts` / `deal.ends` as VEVOR gives them) or
when VEVOR's page shows its own strikethrough price, otherwise `None`: never
compute a discount from it. Search and listing totals are exact up to 100 and
then read "100+" (`total_is_lower_bound`). Reviews are one pool shared across
storefronts and a product's variants, so they come in many languages, fully
paged up to 100 a page, with no reviewer names. Not available: coupon codes
(VEVOR shows them only after a claim), the pickup store, Pro or bulk prices,
financing, the ships-from warehouse, VEVOR's listings on other marketplaces
(use those namespaces), price history (poll and store the answers), checkout.
Failed calls and refused inputs are not charged; a not-found (an unknown SKU
or category, or a SKU the storefront does not sell) is charged.

### 76. Liquidation auctions -- Nellis Auction lot prices, bid history, sold prices

Nellis Auction (nellisauction.com, the liquidation auction marketplace with
pickup warehouses in Las Vegas, Phoenix, Houston, Philadelphia, Denver and
Dallas). Namespace `nellis`, 4 endpoints: `search`, `item`, `locations`,
`categories`. 1 credit per call; `credits_used` in the response is what was
charged. `search`, `locations` and `categories` take `location` (default
`las-vegas`); `item` takes an `id` or a `url`. The request timeout is raised
to at least 240s. Nellis Auction has no public API. Pair a lot with the
`amazon` and `walmart` namespaces for the same item's new price and with
`ebay` for sold prices (match on title and brand: Nellis shows no UPC). See the
[Nellis Auction API page](https://scavio.dev/nellis-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
nl = client.nellis

# --- Open auctions in one shopping location: current bid, bids, Estimated Retail Price, close time.
hits = nl.search("robot vacuum")["data"]
print(hits["location"], hits["total"], hits["has_more"])
for it in hits["items"][:5]:
    print(it["id"], it["title"], it["current_bid"], it["bid_count"], it["retail_price"], it["closes"])
# Another location, most bids first, 48 a page.
phx = nl.search("vacuum", location="phoenix", sort="bids_high", page_size=48)["data"]

# --- One lot, open or sold: final price of a sold lot (before the premium), bid history.
lot = nl.item("141100004")["data"]
print(lot["market_status"], lot["final_price"], lot["retail_price"], lot["buyer_premium_percent"])
for b in lot["bid_history"]:
    print(b["time"], b["amount"], b["status"])

# --- Pickup warehouses with hours, and live category / brand / auction-event counts.
wh = nl.locations(location="las-vegas")["data"]
for w in wh["locations"]:
    print(w["name"], w["city"], w["state"], w["hours"]["monday"])
cats = nl.categories(location="houston", category="Electronics")["data"]
print(cats["total_open_items"], cats["subcategories"][:3])
```

Shopping locations (`location`): `las-vegas`, `phoenix`, `houston`,
`philadelphia` (pickup in Delran, NJ), `denver` and `dallas` (run by Lots Of
Auctions), with 13 pickup warehouses in all. Search lists open auctions only,
as Nellis's own search does; a closed or sold lot is read by id with `item`,
and a sold lot's `final_price` is the winning bid before Nellis's buyer's
premium and tax. `retail_price` is Nellis's own "Estimated Retail Price", as
Nellis labels it, not an MSRP. The buyer's premium is, in Nellis's words,
"typically 15% but may vary based on the auction event"
(`buyer_premium_percent` per lot). Captured 2026-11-25: a sold lot (id
141100004, Estimated Retail Price 9.99) closed at a final price of 6 after 5
bids. Bids move live: `current_bid`, `bid_count` and `closes` are as of the
fetch. `bid_history` gives time, amount and Winning or Outbid, with no bidder
names. Not available: closed or sold lots in search, search suggestions,
shipping (pickup only), UPC or model numbers, buy-now, reserve prices, live
bid updates, bidding, watchlists and checkout. Failed calls and refused inputs
are not charged; a not-found (an unknown id, or a category with no open lots)
is charged.

### 77. Skincare -- Dermstore prices, offers by brand, US vs Canada

Dermstore (dermstore.com, the US skincare and beauty retailer, shipping to
the US and Canada). Namespace `dermstore`, 7 endpoints: `search`, `list`,
`product`, `suggestions`, `offers`, `brands`, `categories`. 1 credit per
call; `credits_used` in the response is what was charged. Every method takes
`country` (`us` default, prices in USD; `ca`, Dermstore's own Canadian dollar
prices, not converted). The request timeout is raised to at least 240s.
Dermstore has no public API; its affiliate programme runs on Awin and offers
product feeds to approved publishers. Pair a product with the `sephora`,
`ulta` and `amazon` namespaces for the same product and size elsewhere (match
on UPC, or brand + name + size). See the
[Dermstore API page](https://scavio.dev/dermstore-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
dm = client.dermstore

# --- Search: price, RRP, Dermstore's offer text per product.
hits = dm.search("uv clear spf 46")["data"]
print(hits["market"], hits["total"], hits["has_more"])
for it in hits["items"][:5]:
    print(it["sku"], it["name"], it["price"], it["rrp"], it["discount_percent"], it["offer"])
# The same search in Canada: Dermstore's own CAD prices.
ca = dm.search("uv clear spf 46", country="ca")["data"]
# A mapped keyword returns the page Dermstore sends it to.
sun = dm.search("sunscreen", sort="discount", page_size=100)["data"]
print(sun["resolved_from"])

# --- Any list page: a brand, /sale or an offer page.
brand = dm.list("/brands/eltamd", include_facets=True)["data"]

# --- One product: variants with their own price and stock, UPC, offer banner, 10 latest reviews.
p = dm.product("13806521")["data"]
print(p["price"], p["rrp"], p["upc"], p["offer"]["title"], p["auto_replenish"])
for v in p["variants"]:
    print(v["sku"], v["option"], v["price"], v["in_stock"])

# --- Current offers with their end times, brands and categories.
for o in dm.offers()["data"]["offers"]:
    print(o["title"], o["code"], o["threshold"], o["ends"], o["list_path"])
brands = dm.brands(letter="E")["data"]
cats = dm.categories()["data"]
```

`rrp` is Dermstore's RRP as given; `discount_percent` is computed by Scavio
from price and RRP, only when the RRP is above the price. `offer` is
Dermstore's own promotion text, as given; code rates differ by brand.
Captured 2026-11-25: EltaMD UV Clear Broad-Spectrum SPF 46 (1.7 fl. oz., SKU
11370303) at 46 USD and 65.78 CAD; Medik8 offered "30% Off With Code JOY +
Gift", while SkinCeuticals offered "Earn 10% Back + $25 Gift" (double points,
as Dermstore states it). A mapped keyword (sunscreen, retinol, eltamd) returns
the products of the page Dermstore sends it to, reported in `resolved_from`.
Offers carry the end time Dermstore gives (`ends`); Dermstore gives no start
date. Not available: a full review feed or review paging (only the 10 latest
via `product`), Q&A, member (VIP) prices, cart or checkout prices, price
history (poll and store the answers), offer start dates. Failed calls and
refused inputs are not charged; a not-found (an unknown SKU or list path) is
charged.

### 78. Local marketplace -- OfferUp asking prices by city, cars and trucks, sellers

OfferUp (offerup.com, the US local marketplace for buying and selling used
items, cars and trucks). Namespace `offerup`, 5 endpoints: `search`,
`listing`, `category`, `categories`, `seller`. 1 credit per call; `listing`
is 1, or 2 when the listing needs a second, costlier fetch. `credits_used` in
the response is what was charged. US only (no `country`), prices in USD.
`search` and `category` take a US ZIP (required). The request timeout is
raised to at least 240s. OfferUp has no public API for reading listings;
OfferUp for Business (OfferUp Motors, Storefronts) is seller-side tooling
that syncs a dealer's own inventory into OfferUp. Pair a listing with the
`amazon` and `walmart` namespaces for the same item's new price and with
`mercari` sold search for sold prices (match on model and title). See the
[OfferUp API page](https://scavio.dev/offerup-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ou = client.offerup

# --- The same keyword in two US metros: asking prices around each ZIP.
for zip_code in ("98101", "60601"):
    feed = ou.search("iphone 15", zip_code)["data"]
    print(feed["location"]["resolved"], feed["location"]["radius_miles"], feed["count"], feed["has_more"])
    for it in feed["items"][:5]:
        print(it["listing_id"], it["title"], it["price"], it["city"], it["state"], it["sponsored"])
    print(feed["filters_not_applied"])

# --- Cars and trucks: dealer listings, model year, mileage.
trucks = ou.search("toyota tacoma", "75201", seller_type="dealer", year_min=2018,
                   max_mileage=100000, sort="lowest_mileage")["data"]
for it in trucks["items"][:5]:
    print(it["title"], it["price"], it["vehicle_miles"])

# --- One listing: condition, posted date, vehicle details (no VIN), seller numbers.
li = ou.listing("7a392126-fb9d-34c2-a6d8-1b94698428df")["data"]
print(li["price"], li["condition"], li["posted_at"], li["vehicle"], li["seller"]["seller_type"])

# --- A category around a ZIP, the category tree and a seller's public profile.
furniture = ou.category("furniture", "90012")["data"]
tree = ou.categories()["data"]
dealer = ou.seller("8668343")["data"]
print(dealer["rating"], dealer["rating_count"], dealer["items_sold"], dealer["count"])
```

`location.resolved` is the area OfferUp named for the ZIP and
`location.radius_miles` the radius it applied (captured 2026-11-25: 98101
resolved to Seattle, 60601 to Chicago, both 30 miles). Captured 2026-11-25:
"toyota tacoma" around 75201 (Dallas, 80 miles) with `seller_type="dealer"`,
`year_min=2018`, `max_mileage=100000` and `sort="lowest_mileage"` listed a 2025
Toyota Tacoma 2WD at 35495 USD with 10017 miles. `filters_not_applied` lists
any filter OfferUp did not apply to the feed; `seller_type` applies in Cars &
Trucks only (on search it limits the results to category 5.1). Promoted
OfferUp listings are marked `sponsored`. About 48 listings a page up to page
50, no total count (`has_more`). Search tiles carry no posted date or
condition (`listing` does). Prices are asking prices, not sold prices.
Private sellers: no seller names (a dealer or business account's name only),
usernames, avatars, phone numbers, emails, street addresses, coordinates or
VINs; phone numbers, emails and VIN-like codes in titles and descriptions read
`[removed]`. Not available: sold listings or sold prices (OfferUp does not
show them publicly), shipping (OfferUp ended nationwide shipping in 2025;
listings are local pickup), search suggestions, a total result count, a
seller's listings past the first 20, messaging or offers. Failed calls and
refused inputs are not charged; a not-found (an unknown listing, category or
seller) is charged.

### 79. Canadian sporting goods and workwear -- SportChek and Mark's prices, sale dates, stock

SportChek (sportchek.ca, Canada's sporting goods retailer, a Canadian Tire
Corporation banner) and Mark's (marks.com, the Canadian workwear, casual
clothing and footwear retailer, a Canadian Tire Corporation banner; L'Equipeur
in French). Namespaces `sportchek` and `marks`, 8 endpoints each:
`search`, `list`, `product`, `suggestions`, `store`, `brands`, `categories`,
plus `reviews` on SportChek and `questions` on Mark's. 1 credit per call on
every endpoint; `credits_used` in the response is what was charged. Canada
only, prices in CAD. Answers take about 10-90 seconds: the request timeout is
raised to at least 240s, so allow up to 2 minutes per call. Mark's takes
`language="fr"` on `search`, `list`, `product`, `brands` and `categories` to
read L'Equipeur (lequipeur.com): the same product codes and CAD prices, French
titles. SportChek is English only. Neither banner has a public API. Pair a
product with the `amazon` and `walmart` namespaces for the same model at
Amazon.ca and Walmart.ca (match on brand, model, colour and size). See the
[SportChek API page](https://scavio.dev/sportchek-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) and the
[Mark's API page](https://scavio.dev/marks-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
sc = client.sportchek

# --- Search: price, was price, sale label and end date, with the site's own footnote.
res = sc.search("winter jacket", include_facets=True)["data"]
print(res["total"], res["total_pages"], res["footnote"])
for it in res["items"][:5]:
    print(it["code"], it["name"], it["price"], it["was_price"], it["sale_ends"], it["badges"])

# --- Filters come from facets; deals pages and categories are list() paths.
women = sc.search("winter jacket", filters=[{"facet": "sku_gender_attr", "value": "Female"}],
                  deals="sale")["data"]
clearance = sc.list("/en/sale-clearance/clearance.html", sort="price_low")["data"]

# --- One product: each variant's price, was price, sale_ends and units.
p = sc.product("84166659F")["data"]
print(p["price"], p["sale_ends"], p["assigned_store"])
for v in p["variants"][:5]:
    print(v["colour"], v["size"], v["price"], v["units_at_store"], v["units_online"])

# --- SportChek reviews: summary, then pages of 8, 30, 30, 30.
rv = sc.reviews("84166659F")["data"]
print(rv["summary"]["average"], rv["summary"]["count"], rv["max_page"])

# --- Mark's, in English and in French (L'Equipeur), and its customer questions.
mk = client.marks
en = mk.product("75983776F")["data"]
fr = mk.product("75983776F", language="fr")["data"]
print(en["name"], en["price"], en["was_price"], "|", fr["name"], fr["price"])
qa = mk.questions("75984589F")["data"]
store = mk.store("589")["data"]
print(qa["total"], store["name"], store["nearby_count"])
```

`was_price` is the site's was price as given, only where the site shows one;
`footnote` is the site's own sentence on it ("Was price reflects the last
national regular price this product was sold for.", English pages). A percent
off is not returned: compute it from `price` and `was_price` and label it
computed. `sale_ends` is the sale end date the site shows, as given;
`price_message` is the site's promotion text. `units_at_store` are the units at
the store the site assigns to the request's region (`assigned_store`); a caller
cannot choose a store. In our checks prices were the same at every store
sampled. Captured 2026-11-25: SportChek's Columbia Women's Amaze Puff Down
Jacket (84166659F) at 206.24 CAD with the promotion "25% Off* - Discount
Applied. See details." and `sale_ends` December 1, 2026 (29 variants;
assigned store 237, Cornwall, ON); Mark's Dakota WorkPro Series 6114 work
boots (75983776F) at 124.99 CAD with a was price of 199.99 and `sale_ends`
November 25, 2026, the same price and code on L'Equipeur with a French title.
Search and list pages are 24 products (12 on Mark's category pages),
`page_size` says; `deals` on a deals page is a 400 (the page already is one).
SportChek reviews: page 1 is the first 8, pages 2-4 the next 30 each (up to 98
per sort and star filter), no reviewer names. Mark's questions: the newest 10
with answers, no asker names. `store` returns one store by number with up to
49 nearby stores. Not available: choosing a store for price or stock, stores
near a postal code, Mark's reviews, SportChek questions, the flyer, Triangle
Rewards or CT Money prices, price history (poll and store the answers), UPC or
barcodes (the site shows none), cart or checkout. Failed calls and refused
inputs are not charged; a not-found is charged.

### 80. Home Depot Canada -- prices and exact units per store, store vs online price

Home Depot Canada (homedepot.ca, The Home Depot's Canadian store: 182 stores in
10 provinces) is on the existing `home_depot` namespace. Pass `country="ca"` to
`search`, `product`, `reviews`, `stores` and `availability`; `category`,
`categories`, `stock`, `store` and `suggestions` are Home Depot Canada only and
need no country. `shipping` is US only (`country="ca"` is a 400, not charged). 1 credit per
call on every Canada call (the US stays at 2). Prices in CAD as Home Depot
Canada gives them; `language="fr"` returns French names and links with the same
ids and prices. Home Depot Canada has no public API. See the
[Home Depot API page](https://scavio.dev/homedepot-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()

# Search priced at one store: every product carries store_units and aisle / bay.
hits = client.home_depot.search("cordless drill", country="ca", store_id="7080")

# One item at a store: price is that store's price, online_price the online one.
stud = client.home_depot.product("1000112108", country="ca", store_id="7128")
print(stud["data"]["price"], stud["data"]["price_source"], stud["data"]["online_price"])

# One item at one store: the store's price, exact units, aisle and bay.
at_store = client.home_depot.availability("1001769719", store_id="7076", country="ca")

# Stores near a postal code or city (or latitude / longitude).
stores = client.home_depot.stores("M5V 2T6", country="ca")

# Exact units at every store near a postal code (no prices).
stock = client.home_depot.stock("1001769719", "H3B 1A1")
for s in stock["data"]["stores"]:
    print(s["store_id"], s["name"], s["units"])

tree = client.home_depot.categories(depth=2)
trees = client.home_depot.category("661103", store_id="7128", sort_by="price_low")
store = client.home_depot.store("7076")
words = client.home_depot.suggestions("christ")
```

Captured 2026-11-25: the 2-inch x 4-inch x 8-ft SPF Premium Stud (1000112108)
at store 7128 (ST-HENRI, QC) at 4.14 CAD (`price_source: "store"`) with 2858
units in aisle 19, bay 001, next to an `online_price` of 6.58. Prices can differ
by store (lumber does; the tools, Christmas tree and fridge sampled had one
price everywhere), and the online price can differ from a store's price.
Search takes `store_id` (default store 7274; `data.store` says which),
`page_size` 1-40, the sorts `best_match`, `price_low`, `price_high` and
`top_rated` (`top_sellers` is a 400 for Canada), facet `filters` from
`include_facets`, and `deals` (`special_buy`, `new_lower_price`, `savings`);
with `category_id` or `deals` the query is optional. `reviews` returns the
first 8 reviews per language and the first page of questions (page 2 is a 400;
no reviewer names). When Home Depot Canada has no store record for an item that
exists, `product` returns the online price with `store_price_returned: false`
and `availability` and `stock` answer an unbilled 502. Not available for Canada: UPC or barcodes
(Home Depot Canada shows none), structured sale end dates (the price badge and
Home Depot's promotion text only), delivery quotes (`shipping` is a 400 for
`ca`), the flyer, cart or checkout, price history (poll and store the answers).
For the same item at other Canadian retailers use the `canadian_tire`, `walmart`
(`domain="ca"`) and `amazon` (`country="ca"`) namespaces; match on brand and
model.

### 81. Best Buy Canada -- exact units per store, EHF by province, sale end dates

Best Buy Canada (bestbuy.ca, Best Buy's Canadian store: 142 stores across Canada
per Best Buy's FY2026 10-K, plus a marketplace of third-party sellers) is on the
existing `best_buy` namespace. Pass `country="ca"` to any of the nine methods;
`questions` is Best Buy Canada only and needs no country. 1 credit per call on
every Canada call (US credits are unchanged). Prices in CAD as Best Buy Canada
gives them; `language="fr"` returns French names, specs and links with the same
SKUs and prices. Best Buy's developer API (developer.bestbuy.com) covers
bestbuy.com only. See the
[Best Buy API page](https://scavio.dev/bestbuy-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
bb = client.best_buy

# Search: CAD price, regular price, savings, sale_ends_at and the ehf for province.
tvs = bb.search("4k tv", country="ca", sort="price_low", province="QC")["data"]
print(tvs["total_results"], tvs["results_capped"], tvs["products"][0]["price"])

# One product: UPC, sale start / end (UTC), EHF by province, open-box SKUs.
mac = bb.product(sku="19791103", country="ca")["data"]
print(mac["upc"], mac["price"], mac["regular_price"], mac["sale_ends_at"])
print(mac["ehf_by_province"], [(o["sku"], o["condition"], o["price"]) for o in mac["open_box"]])

# Exact units per store near a postal code (no prices: they are national).
avail = bb.availability(sku="19791103", country="ca", postal_code="H3B 4W8", max_stores=5)
for store in avail["data"]["products"][0]["stores"]:
    print(store["store_id"], store["name"], store["city"], store["units"], store["status"])

# Deal collections, stores, prices for up to 20 SKUs, and questions.
bf = bb.deals(country="ca", collection="black_friday")["data"]
print(bf["dates_text"])
stores = bb.stores(country="ca", postal_code="M5V 3L9")
prices = bb.prices(["19791103", "19296507"], country="ca")
qa = bb.questions(sku="19296507", sort="most_answered")
```

Captured 2026-11-25: the Apple MacBook Air 13.6" (2026, M5, 16GB / 512GB, SKU
19791103) at 1589.99 CAD (regular 1789.99, `sale_ends_at` 2026-12-03T07:00:00Z),
with 35 units in the Centreville store in Montreal (store 651). The price is
national (the same in every province and store); only the environmental
handling fee varies by province (`province`, default `ON`; `ehf_by_province` on
product and prices). A store with no stock record for the SKU comes back
`status: "unknown"` with `units: None`, never out of stock. Listings take
`page_size` 1-100 (default 24), the sorts `best_match`, `price_low`,
`price_high` and `rating` (`best_selling`, `best_discount` and `newest` are a
400 for Canada) and the extra filters `rating`, `sold_by`, `seller`,
`in_stock_online` and `facets`; results are capped at the first 2,000 of a query
(`results_capped`). Marketplace sellers come back named as Best Buy Canada lists
them. Product `rating` and `review_count` are null (read them from `reviews` or
`prices`). `deals` takes a collection (`black_friday`, `top_deals`,
`clearance`, `open_box`, `refurbished`); `dates_text` carries the collection's
own dates when its page states them ("Sale kicking off November 19 and running
until December 3" on the Black Friday collection). Not available for Canada:
per-store prices (the price is national), a Deal of the Day (Best Buy Canada has
none), results past 2,000 per query, review photos hosted off Best Buy, cart or
checkout, price history (poll and store the answers). For the same model at
other Canadian retailers use the `amazon` (`country="ca"`), `walmart`
(`domain="ca"`), `costco` (`country="ca"`) and `canadian_tire` namespaces; match
on brand and model.

### 82. Sephora Canada -- CAD prices, sale prices, dated offers, stores

Sephora Canada (sephora.com/ca, Sephora's Canadian store: 152 stores per its
store list on Nov 25, 2026) is on the existing `sephora` namespace. Pass
`country="ca"` to `search`, `category` and `product`; `brand`, `brands`,
`suggestions`, `offers`, `stores` and `store` are Sephora Canada only and need no
country. Canadian beauty prices in CAD (The Ordinary, Dior, Rare Beauty,
Supergoop and the rest of the catalogue) with sale prices and dated offers.
Credits: `search`, `category`, `brand`, `brands`, `suggestions`, `stores` and
`store` 1 each; `product` and `offers` 2 (US credits are the same and
unchanged). Product and SKU ids are the same as on sephora.com, with CAD prices
as Sephora Canada gives them (French prices such as `33,00 $` are read as
33.00); `language="fr"` returns French names, descriptions and facet values with
the same ids and prices. Sephora publishes no public product or store API. See
the
[Sephora API page](https://scavio.dev/sephora-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
seph = client.sephora

# Search: CAD price, list and sale price, sale scope, filters and facets.
oils = seph.search("lip oil", country="ca", filters={"on_sale": True}, include_facets=True)["data"]
for p in oils["products"]:
    print(p["product_id"], p["brand"], p["price"], p["list_price"], p["sale_price"], p["name"])

# One product: every SKU with price, sale price, in_stock and only_few_left.
item = seph.product(product_id="P428500", country="ca")["data"]
for sku in item["skus"]:
    print(sku["sku_id"], sku["size"], sku["price"], sku["in_stock"], sku["only_few_left"])
print(item["review_summary"]["source"])          # Sephora's own AI summary, labelled
print(len(item["latest_reviews"]))               # the 10 latest, no reviewer names

# Brands, a brand's products, suggestions, dated offers and stores.
brands = seph.brands()["data"]["brands"]
ordinary = seph.brand("the-ordinary", sort="best_selling")["data"]
terms = seph.suggestions("lip")["data"]["terms"]
for o in seph.offers()["data"]["offers"]:
    print(o["title"], o["eligibility"], o["promo_code"], o["end_date"], o["app_only"])
quebec = seph.stores(province="QC")["data"]
store = seph.store("toronto-eaton-centre")["data"]["store"]
print(store["address"], store["phone"], store["hours"])
```

Captured 2026-11-26: Dior Sauvage Eau de Parfum (`P428500`) at 128 to 300 CAD,
the 3.4 oz / 100 ml SKU 2038131 at 200 CAD with `in_stock: True` and
`only_few_left: False`; the Sephora Collection Oil Infusion Hydrating Lip Oil
(`P518068`) at a sale price of 10.50 CAD (list 15.00) in a `lip oil` search;
26 offers, among them 30% off Sephora Collection with `end_date`
2026-11-30T23:59:00.000-08:00; and 152 stores on the store list (ON 64, QC 26,
AB 22, BC 22). Listings take `sort`, `filters` (`brand`, `on_sale`, `new`,
`clean`, `rating` 1-4, `min_price`, `max_price`, `facets`, or a list of
`{"facet", "value"}`) and `include_facets`; a brand keyword such as
`the ordinary` answers that brand's products with a `redirect`. `zip` is US
only (a 400 with `country="ca"`). `review_summary` is Sephora's own
AI-generated summary of customer reviews and is labelled as Sephora's; read it
as Sephora's summary, not as a fact. Offers carry `end_date` as given and no
start date; app-only offers are flagged `app_only`. Store address and phone are
public business data, returned as captured. Not available for Canada: stock per
store, a store finder by postal code, the full review list with its sorts or a
star filter, UPC (`upc` is always `None`: the pages show none), Beauty Insider
prices, cart or checkout, price history (poll and store the answers). For the
same product at other Canadian retailers use the `dermstore`
(`country="ca"`), `amazon` (`country="ca"`) and `walmart` (`domain="ca"`)
namespaces; match on brand, name and size.

### 83. Canadian home improvement -- RONA store prices, exact units, stores

RONA (rona.ca, the Canadian home improvement retailer: RONA+ and RONA stores,
about 425 corporate and affiliated dealer stores per RONA inc.). Namespace
`rona`, 9 endpoints: `search`, `product`, `prices`, `category`, `categories`,
`stores`, `store`, `stock`, `deals`. Credits: `prices`, `categories`, `stores`
and `store` 1; `search` and `deals` 2 (3 with `store_id`; `search` 2 more when
RONA redirects the term); `product` 3; `stock` 3; `category` 2 (3 with
`store_id`), or 1 with `family_id` and `store_id`. `credits_used` in the
response is what was charged. Canada only, prices in CAD; `language` is `en`
(default) or `fr` on every method. Answers can take up to about a minute: the
request timeout is raised to at least 240s. RONA has no public API. Pair a
RONA item with the `home_depot` namespace and `country="ca"` for Home Depot
Canada in the same city: match the same grade and length, or the same model.
See the [RONA API page](https://scavio.dev/rona-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
rn = client.rona

# --- Find stores: by province, city or banner, or nearest a point.
near = rn.stores(latitude=43.6426, longitude=-79.3871, limit=5)["data"]
for s in near["stores"]:
    print(s["store_id"], s["name"], s["banner"], s["relationship"], s["distance_km"])

# --- The same articles at three stores (up to 60 articles per call, 1 credit).
skus = ["0971073", "0938002", "0938042", "00277649"]
for store_id in ("41460", "55130", "62860"):
    res = rn.prices(skus, store_id)["data"]
    for it in res["items"]:
        print(store_id, it["sku"], it["name"], it["price"], it["regular_price"],
              it["on_sale"], it["units"], it["aisle"])

# --- Search and deals priced at one store (store.requested says whose prices).
hits = rn.search("2x4", store_id="41460")["data"]
print(hits["total"], hits["store"], hits["items"][0]["price"])
deals = rn.deals(store_id="55130")["data"]

# --- One product: the sale end as RONA shows it, store units and aisle.
p = rn.product("00277649", store_id="55130")["data"]
print(p["price"], p["regular_price"], p["rebate"], p["sale_ends_text"], p["sale_ends"])

# --- Which stores near a store have an article.
st = rn.stock("00277649", "62860")["data"]
print(st["count"], st["in_stock_count"], [(s["name"], s["units"]) for s in st["stores"][:3]])
```

Without `store_id`, `search`, `category` and `deals` are priced at the store
RONA's site picks for the visit (`store.requested` false); with `store_id`
prices and units are that store's. RONA prices some goods per store: captured
2026-11-26, 2-in x 4-in x 8-ft SPF Select Lumber (0971073) was 4.35 CAD at
store 41460 (Quebec), 4.22 at 55130 (Ontario) and 4.19 at 62860 (Alberta),
while the DEWALT 20 V MAX Brushless Compact Drill/Driver Kit on sale
(00277649) was 118 (regular 219) at all three. `units` are exact store units;
`None` means RONA showed no count, not zero. Article numbers are strings
(leading zeros count). `product` returns `sale_ends_text` as RONA shows it
("until Dec 10th, 2026") and `sale_ends` as an ISO date only when it is
unambiguous; rating and review count only, no review text. `stores` covers
the 403 stores on RONA's store locator (RONA+ and RONA; corporate and dealer).
`stock`: RONA offers no nearby-store list for some articles (lumber), and the
list can come back empty now and then (call once more). Not available: review
text, search suggestions, postal-code store lookup (pass latitude and
longitude, or a city or province), the printed flyer, cart or checkout, price
history (poll and store the answers). Failed calls and refused inputs are not
charged; a not-found (an unknown article, category or store) is charged.

### 84. Canadian grocery -- PC Express prices by banner, deals, stores

PC Express (Loblaw's online grocery for Real Canadian Superstore, No Frills,
Loblaws, Zehrs, Fortinos, Valu-mart, Your Independent Grocer, Wholesale Club,
Provigo and Maxi; Loblaw operates 2,504 stores per its 2025 annual report).
Namespace `pcexpress`, 7 endpoints: `search`, `category`, `collection`,
`product`, `stores`, `store`, `suggestions`. The job: what each Loblaw banner
charges for the same product code at its default store on one date, with the
deal end date and the PC Optimum offer as shown. Credits: `search`,
`category`, `collection`, `stores` and `suggestions` 1; `product` 5 (1 when it
answers from the search listing, `source` "search"); `store` 5.
`credits_used` in the response is what was charged. Canada only, prices in
CAD. Answers can take up to about a minute; allow up to 2 minutes for
`product`, `store`, `stores` and `suggestions`: the request timeout is raised
to at least 240s. PC Express has no public API. Pair a national-brand item with the
`walmart` namespace and `domain="ca"` for Walmart.ca, and see the `costco`,
`instacart` and `amazon` namespaces.
See the [PC Express API page](https://scavio.dev/pcexpress-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
pcx = client.pcexpress

# --- The same product code on three banners (each banner's default store).
for banner, query, language in (("superstore", "eggs", "en"), ("nofrills", "eggs", "en"),
                                ("maxi", "oeufs", "fr")):
    res = pcx.search(query, banner=banner, language=language)["data"]
    for it in res["items"]:
        if it["code"] == "20812144001_EA":
            print(banner, res["store"]["store_id"], it["name"], it["price"], it["unit_price"])

# --- Deals with their end date and PC Optimum offer as shown.
deals = pcx.collection("deals-centre", banner="nofrills")["data"]
for it in deals["items"][:5]:
    print(it["name"], it["price"], it["was_price"], it["deal"], it["pc_optimum_points"])

# --- One product: GTIN, nutrition, comparison prices.
p = pcx.product("20812144001_EA")["data"]
print(p["source"], p["gtin"], p["price"], p["comparison_prices"], p["stock_status"])

# --- Pickup stores and one store's hours.
stores = pcx.stores(city="Winnipeg")["data"]
store = pcx.store("1517")["data"]
print(stores["matched"], store["name"], store["store_hours"][0])
```

`banner`: `superstore` (Real Canadian Superstore, default), `nofrills`,
`loblaw` (Loblaws), `zehrs`, `fortinos`, `valumart` (Valu-mart),
`independent` (Your Independent Grocer), `wholesaleclub` (Real Canadian
Wholesale Club), `provigo`, `maxi`. `language` is `en`, or `fr` on `provigo`
(French only) and `maxi` (French by default, English too). Prices are each
banner's default online store's; choosing a store is not offered (a `store_id`
on a priced method is a 400, not charged), and every answer says which store
priced it in `store` (`requested` false). The same product code is priced per
banner: captured 2026-11-26, No Name Large Size Eggs 12 Pack (20812144001_EA)
was 3.93 CAD at Real Canadian Superstore's default store 1033 and 4.17 at
Maxi's default store 8976. `deal` carries the end date PC Express shows
(`expiry_date`), no start date; `pc_optimum_points` is the PC Optimum offer as
shown; `member_only_price` is the price the site shows publicly on the item,
not a price behind a login. `product` adds GTIN, ingredients, nutrition,
comparison prices and stock status as given. `stores` lists a banner's pickup
stores (city, postal code start, province, or nearest a point); `store` gives
7 dated days of store, pharmacy, clinic and optical hours. Not available:
choosing a store, review text (rating and count only), the printed flyer,
Shoppers Drug Mart, Atlantic Superstore, City Market and T&T, cart or
checkout, PC Optimum prices behind a login, price history (poll and store the
answers). Failed calls and refused inputs are not charged; a not-found (an
unknown code, category, collection or store) is charged.

### 85. Luxury beauty -- Space NK prices in four markets, reviews, UK store availability

Space NK (spacenk.com, the London-based luxury beauty retailer, owned by Ulta
Beauty): search, category and brand listings with the price, the
struck-through price, discount and promo badges and online stock of the shade
or size shown; one product with every shade or size, EAN, promotions and
ingredients; customer reviews (no reviewer names); search-box suggestions; the
UK stores near a postcode for one product (in-store flag and Click & Collect,
not unit counts); and the gifts with purchase on the offers page. Markets uk
(GBP, default), ie (EUR), nl (EUR, Dutch copy) and au (AUD), each priced in
its own currency; the US market is not offered (Space NK's US path shows UK
prices). Brand ids are Space NK's own (from `brands`); `stores` is UK only and
takes a `product_id`; reviews are kept per master product id (starting with
M); `offers` is uk or ie. Namespace `spacenk`, 9 endpoints: `search`,
`category`, `brand`, `brands`, `product`, `reviews`, `suggestions`, `stores`,
`offers`. Credits: 1 credit each; `search`, `category` and `brand` with
`full=True` up to 5 (one more call per product filled). `credits_used` in the
response is what was charged. The request timeout is raised to at least 240s.
Space NK has no public API.
See the [Space NK API
page](https://scavio.dev/spacenk-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/spacenk-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
sn = client.spacenk
hits = sn.search("vitamin c serum", market="uk")["data"]
for it in hits["items"][:5]:
    print(it["product_id"], it["name"], it["price"], it["list_price"], it["currency"])
p = sn.product("MUK200057800", market="ie")["data"]
print(p["price"], p["currency"], p["stock_count"], len(p["variants"]))
near = sn.stores("MUK200057800", postcode="W1D 1BS")["data"]
for s in near["stores"][:3]:
    print(s["name"], s["distance_miles"], s["in_store_available"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 86. Beauty on 10 country sites -- Lookfantastic prices, variants, barcodes, voucher codes

Lookfantastic (lookfantastic.com, THG's beauty retailer with 10 country
sites): keyword or SKU search and any list page (category, brand, sale, Black
Friday) with the price, RRP, discount, offer text and filters (brand, skin
type, concern, SPF, key ingredient, formulation, price, rating, discount); one
product with every variant's own price and stock and its barcode (EAN-13 or
UPC, as given); search suggestions; the voucher-codes page with end times; the
A-Z brand directory and the category tree. `market` picks the site (gb for
lookfantastic.com with 22 currencies, de, fr, es, it, nl, pl, at, ie, eu) and
`currency` one of that site's own currencies. The search keyword is `query` in
Python and `q` on the wire (and in the TypeScript options). Namespace
`lookfantastic`, 7 endpoints: `search`, `list`, `product`, `suggestions`,
`offers`, `brands`, `categories`. Credits: 1 credit each. `credits_used` in
the response is what was charged. The request timeout is raised to at least
240s. Lookfantastic has no public API.
See the [Lookfantastic API
page](https://scavio.dev/lookfantastic-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/lookfantastic-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
lf = client.lookfantastic
hits = lf.search("glow tonic", market="gb", currency="EUR")["data"]
for it in hits["items"][:5]:
    print(it["sku"], it["name"], it["price"], it["rrp"], it["discount_percent"], it["currency"])
p = lf.product("11200055", market="de")["data"]
print(p["price"], p["barcode"], [(v["option"], v["price"]) for v in p["variants"]])
offers = lf.offers(market="gb")["data"]["offers"]
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 87. Beauty in 12 currencies -- Cult Beauty prices, variants, barcodes, voucher codes

Cult Beauty (cultbeauty.co.uk, THG's beauty retailer): keyword or SKU search
and any list page with the price, RRP, discount, offer text and filters
(brand, skin type, concern, SPF, key ingredient, formulation, range, price,
rating, discount); one product with every variant's own price and stock and
its barcode; search suggestions; the voucher-codes page with end times; the
A-Z brand directory and the category tree. `market` is gb (cultbeauty.co.uk)
or intl (cultbeauty.com), each in 12 currencies; `offers` is not available on
intl (a 400, not charged). Namespace `cultbeauty`, 7 endpoints: `search`,
`list`, `product`, `suggestions`, `offers`, `brands`, `categories`. Credits: 1
credit each. `credits_used` in the response is what was charged. The request
timeout is raised to at least 240s. Cult Beauty has no public API.
See the [Cult Beauty API
page](https://scavio.dev/cultbeauty-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/cultbeauty-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
cb = client.cultbeauty
hits = cb.search("glow tonic", market="gb")["data"]
p = cb.product(hits["items"][0]["sku"], market="intl", currency="USD")["data"]
print(p["name"], p["price"], p["rrp"], p["currency"], p["in_stock"], p["barcode"])
for v in p["variants"]:
    print(v["option"], v["price"], v["in_stock"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 88. Asian beauty -- YesStyle prices per shipping country, deals, reviews

YesStyle (yesstyle.com, the Hong Kong-based online store for Asian beauty and
fashion): keyword search, category, brand and deal lists (Black Friday, flash
sales, clearance, price drops) up to 100 a page with the price, list price,
discount and YesStyle's labels; one product with its sale end date,
ingredients and (with `include_variants`) every shade or size; reviews with
the star summary; suggestions; the brand list and the shipping countries.
YesStyle sets prices per shipping country: `country` (39 countries; 153 on
reviews and suggestions) and the country is checked on every answer. Namespace
`yesstyle`, 9 endpoints: `search`, `category`, `brand`, `brands`, `deals`,
`product`, `reviews`, `suggestions`, `markets`. Credits: `search`, `category`,
`brand`, `deals` and `product` 2 (`product` 3 with `include_variants`);
`brands`, `reviews`, `suggestions`, `markets` 1. `credits_used` in the
response is what was charged. The request timeout is raised to at least 240s.
YesStyle has no public API.
See the [YesStyle API
page](https://scavio.dev/yesstyle-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/yesstyle-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ys = client.yesstyle
hits = ys.search("snail mucin", country="us")["data"]
for it in hits["items"][:5]:
    print(it["product_id"], it["name"], it["price"], it["list_price"], it["currency"])
p = ys.product("1052684695", country="gb", include_variants=True)["data"]
print(p["price"], p["currency"], p["sale_end_date"], p["availability"])
deals = ys.deals(deal="flash_sales", country="au")["data"]
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 89. Perfume and cosmetics -- Notino on 27 storefronts, 30-day lowest price, EAN

Notino (notino.com, the Brno-based online perfume and cosmetics store with 27
country shops): keyword search, category, brand and promo lists (24 a page)
with the price, RRP where shown and stock level; one product with every
variant's price, EAN and the lowest price of the last 30 days; reviews; the
brand directory; search suggestions; and Notino's stores in the 8 markets that
have them. `market` is one of 27 storefronts, each in its own language and
currency; gb (notino.co.uk) costs 2 credits per call. Namespace `notino`, 10
endpoints: `search`, `product`, `reviews`, `category`, `brand`, `promo`,
`brands`, `suggestions`, `stores`, `store`. Credits: 1 credit each (2 on gb);
`category`, `brand` and `promo` 3 (4 on gb) for any page after the first, a
sort or a filter; a `search` Notino answers with a brand or category page read
with the page, sort or filters 3 (4 on gb); `reviews` beyond the newest 8 1 on
every storefront. `credits_used` in the response is what was charged. The
request timeout is raised to at least 240s (`reviews` 250s). Notino has no
public API.
See the [Notino API
page](https://scavio.dev/notino-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/notino-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
nt = client.notino
hits = nt.search("vitamin c serum", market="de")["data"]
for it in hits["items"][:5]:
    print(it["product_id"], it["name"], it["price"], it["currency"], it["stock_level"])
p = nt.product("https://www.notino.de/dior/sauvage-eau-de-parfum-fuer-herren/")["data"]
for v in p["variants"]:
    print(v["variant_name"], v["ean"], v["price"], v["lowest_price_30d"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 90. European beauty -- Douglas prices, was price, RRP and 30-day low on 15 storefronts

Douglas (douglas.de, the Dusseldorf-based beauty retailer): keyword search,
category, brand and deal lists (sale, Beauty / Black Friday) with the price,
the was price, the RRP and the lowest price of the last 30 days; one product
by base or variant code (optionally each variant's EAN); stores and one
store's hours; the review summary (review texts are not available);
suggestions and the brand directory. 15 storefronts in 13 countries (`market`;
it costs 2 credits). Store stock is not available; listings can be slow (the
request timeout is raised to at least 250s). Namespace `douglas`, 10
endpoints: `search`, `category`, `brand`, `deals`, `product`, `stores`,
`store`, `review_summary`, `suggestions`, `brands`. Credits: 1 credit each (2
on it; `stores` and `store` 1 on it too); `product` with `variants_ean` 1 more
per variant looked up (2 on it), up to 10. `credits_used` in the response is
what was charged. The request timeout is raised to at least 250s. Douglas has
no public API.
See the [Douglas API
page](https://scavio.dev/douglas-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/douglas-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
dg = client.douglas
hits = dg.search("mascara", market="at")["data"]
for it in hits["items"][:5]:
    print(it["base_code"], it["name"], it["price"], it["was_price"], it["lowest_price_30d"])
p = dg.product("5000005003", market="de")["data"]
print(p["price"], p["currency"], p["rrp"], p["lowest_price_30d"], p["ean"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 91. UK health and beauty -- Boots prices, offers and store availability

Boots (boots.com, the UK health and beauty retailer, and boots.ie in Ireland):
one product by link or 8-digit id with the price, the was price, the saving,
the unit price, its shades or sizes and the offers Boots names; whether the
Boots stores near a postcode or a point have it (in stock or out of stock per
store, no unit counts); stores near a postcode or a town; and one store's page
with its hours. Markets uk (GBP) and ie (EUR). Search is not available yet:
start from a product link. Namespace `boots`, 4 endpoints: `product`,
`store_stock`, `stores`, `store`. Credits: 1 credit each; 2 when the answer
comes on a second attempt (3 for two-step lookups). `credits_used` in the
response is what was charged. The request timeout is raised to at least 240s.
Boots has no public API.
See the [Boots API
page](https://scavio.dev/boots-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/boots-product?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
bt = client.boots
p = bt.product("https://www.boots.com/no7-protect-and-perfect-intense-advanced-serum-30ml-10288490")
p = p["data"]
print(p["price"], p["was_price"], p["saving"], p["unit_price_text"], p["catentry_id"])
st = bt.store_stock(p["product_id"], p["catentry_id"], postcode="NG2 3AA")["data"]
for s in st["stores"][:5]:
    print(s["name"], s["distance_miles"], s["availability"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 92. Auto parts by vehicle -- RockAuto prices for every brand and tier

RockAuto (rockauto.com, the online auto parts catalog): the vehicle chain
(make, year, model, engine with its `carcode`), a vehicle's part categories
and the parts of one part type with every brand's price, tier, core charge and
pack options; part-number search (OE and interchange numbers too); a brand's
parts; one part's detail; suggestions and a free-text resolver; tools; and
RockAuto's promotions. The US catalog, priced in 15 display currencies
(`currency`), with `language` en, es, fr or de (part detail is English only).
Take `carcode` from the vehicle chain. Namespace `rockauto`, 11 endpoints:
`vehicles`, `categories`, `parts`, `search`, `brand`, `brands`, `part`,
`suggestions`, `resolve`, `tools`, `promotions`. Credits: 1 credit each.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s. RockAuto has no public API.
See the [RockAuto API
page](https://scavio.dev/rockauto-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/rockauto-vehicles?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ra = client.rockauto
engines = ra.vehicles(make="HONDA", year=2010, model="ACCORD")["data"]["engines"]
car = engines[0]  # make, year, model, engine and carcode
parts = ra.parts(car["make"], car["year"], car["model"], car["engine"], car["carcode"],
                 "Brake & Wheel Hub", "1684", currency="CAD")["data"]
for it in parts["items"][:5]:
    print(it["brand"], it["part_number"], it["tier"], it["price"], it["currency"])
hits = ra.search("BP1084")["data"]
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 93. Car listings and dealers -- Cars.com listings, dealer reviews, model reviews

Cars.com (cars.com, the US car marketplace): new, used and certified listings
around a ZIP with the price, mileage, Cars.com's deal labels and the seller;
one listing; a dealer, its inventory and its reviews; model reviews by make,
model and year; dealers near a ZIP; and the research pages. Reviews come
without reviewer names. US only, prices in USD. Namespace `carscom`, 8
endpoints: `search`, `listing`, `dealer`, `dealer_inventory`,
`dealer_reviews`, `model_reviews`, `dealers`, `research`. Credits: 1 credit
each. `credits_used` in the response is what was charged. The request timeout
is raised to at least 240s. Cars.com has no public API for reading listings.
See the [Cars.com API
page](https://scavio.dev/carscom-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/carscom-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
cc = client.carscom
res = cc.search("10001", make="Toyota", model="RAV4", stock_type="used")["data"]
for it in res["items"][:5]:
    print(it["listing_id"], it["title"], it["price"], it["mileage"], it["seller"]["city"])
rev = cc.dealer_reviews(dealer_id="97701")["data"]
print(rev["rating"], rev["total"], [r["rating"] for r in rev["reviews"]])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 94. Car listings -- Autotrader listings, KBB fair price range, price history

Autotrader (autotrader.com, the US car marketplace): listings around a ZIP
with the price, mileage and deal label, filtered by make, model, trim, year,
price, mileage, body style, drivetrain, colors, fuel, history and more; one
listing with features, warranties, the Kelley Blue Book fair price range as
given and price history; dealers near a ZIP; one dealer; and a make's models.
Private sellers come as city and state only. US only, prices in USD; 2 credits
per call. Namespace `autotrader`, 5 endpoints: `search`, `listing`, `dealers`,
`dealer`, `makes`. Credits: 2 credits each. `credits_used` in the response is
what was charged. The request timeout is raised to at least 240s. Autotrader
has no public API.
See the [Autotrader API
page](https://scavio.dev/autotrader-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/autotrader-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
at = client.autotrader
res = at.search("90012", make="Honda", model="Civic")["data"]
for it in res["listings"][:5]:
    print(it["listing_id"], it["title"], it["price"], it["mileage"], it["listing_type"])
car = at.listing(res["listings"][0]["listing_id"], zip="90012")["data"]
print(car["deal_label"], car["deal_basis"], car["price_history"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 95. Car deals -- CarGurus expected price, deal rating and price trends

CarGurus (cargurus.com, the car marketplace in the US, Canada and the UK):
listings around a ZIP or postcode with the price, CarGurus' expected price and
deal rating (the search carries them; there is no listing-detail endpoint); a
dealer's inventory; dealers near a ZIP; price trends for the market, a make or
a model; model-year research pages; expert reviews; makes and models. `market`
is us, us-es, ca, ca-fr or uk. Namespace `cargurus`, 8 endpoints: `search`,
`dealer`, `dealers`, `price_trends`, `research`, `expert_reviews`, `makes`,
`models`. Credits: 1 credit each. `credits_used` in the response is what was
charged. The request timeout is raised to at least 240s. CarGurus has no
public API for reading listings.
See the [CarGurus API
page](https://scavio.dev/cargurus-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/cargurus-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
cg = client.cargurus
res = cg.search("10001", make="Toyota", model="RAV4", sort="best_deal")["data"]
for it in res["listings"][:5]:
    print(it["title"], it["price"], it["expected_price"], it["deal_rating"])
trends = cg.price_trends(make="Toyota", model="RAV4")["data"]
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 96. Used cars -- CarMax no-haggle prices, stores, car value from recent offers

CarMax (carmax.com, the US used-car retailer): inventory near a ZIP with
CarMax's no-haggle price, price drops and shipping fee; one car and its
photos; the 263 stores, one store and a store's inventory; owner reviews and
their summary; suggestions, makes and models; and the car value page (recent
CarMax offers for a model year as shown, not an appraisal of any one car). US
only, prices in USD. Namespace `carmax`, 12 endpoints: `search`, `listing`,
`photos`, `stores`, `store`, `store_inventory`, `reviews`, `review_summary`,
`suggestions`, `makes`, `models`, `car_value`. Credits: 1 credit each.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s. CarMax has no public API.
See the [CarMax API
page](https://scavio.dev/carmax-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/carmax-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
cm = client.carmax
res = cm.search("75201", make="Ford", model="F-150", price_max=30000)["data"]
for car in res["cars"][:5]:
    print(car["stock_number"], car["year"], car["model"], car["price"], car["mileage"])
value = cm.car_value("Ford", "F-150", 2019)["data"]
print(value["aggregate"], value["count"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 97. Used cars online -- Carvana prices, KBB values, shipping costs, model guides

Carvana (carvana.com, the US online used-car retailer): used-car listings by
make and model (24 a page) with the price, the KBB value, shipping cost and
Carvana's labels; one vehicle with its inspection, imperfections and
highlights (no VIN); a model-year guide with owner reviews (no names); a
model's trim guide; a make's lineup and every make in stock. US only, prices
in USD. There is no ZIP targeting: `city` takes one of Carvana's own city
pages (e.g. new-york-ny). Namespace `carvana`, 6 endpoints: `search`,
`vehicle`, `model_guide`, `trims`, `make`, `makes`. Credits: 1 credit each.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s. Carvana has no public API.
See the [Carvana API
page](https://scavio.dev/carvana-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/carvana-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
cv = client.carvana
res = cv.search(make="Toyota", model="RAV4", city="new-york-ny")["data"]
for it in res["items"][:5]:
    print(it["vehicle_id"], it["year"], it["trim"], it["price"], it["kbb_value"], it["shipping_cost"])
car = cv.vehicle(res["items"][0]["vehicle_id"])["data"]
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 98. Collector-car auctions -- Bring a Trailer results and price history

Bring a Trailer (bringatrailer.com, the online collector-car auction site):
completed auction results by keyword, make, model or location (up to 60 a
page, through the first 10,000 results of a query) with the sale price or high
bid; the price history of a model or make in one call with sell-through rate
and per-currency stats; one listing with its bids and comments (no usernames);
live auctions; make, model and location pages; and suggestions. Each lot's
amount is in its own currency, as given. Namespace `bringatrailer`, 8
endpoints: `results`, `price_history`, `listing`, `live`, `make`, `model`,
`location`, `suggestions`. Credits: 1 credit each. `credits_used` in the
response is what was charged. The request timeout is raised to at least 240s.
Bring a Trailer has no public API.
See the [Bring a Trailer API
page](https://scavio.dev/bringatrailer-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/bringatrailer-results?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
bat = client.bringatrailer
hist = bat.price_history(model_id=1833018)["data"]
print(hist["total"], hist["sold_count"], hist["sell_through_rate"], hist["stats_by_currency"])
res = bat.results(query="e30 m3", status="sold")["data"]
for lot in res["lots"][:5]:
    print(lot["title"], lot["amount"], lot["currency"], lot["ended_at"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 99. US rentals -- Rent.com and Apartment Guide rents, deals and city rent trends

Rent.com (rent.com) and Apartment Guide (apartmentguide.com), the US rental
listing sites run by Redfin: rental search by city and state, ZIP or
neighborhood with the rent range per bed count, deals, price drops and the
site's average rents; one rental with floor plans, fees, pet policies, office
hours, schools and walk scores; one building's unit listings; a city's rent
trends by bed count with year-on-year change and the rent spread; search-box
suggestions; and a state's cities. `site` is rent (default) or apartmentguide
(the same rentals). Rents are monthly, in USD. No agent or landlord personal
data is returned. Namespace `rentcom`, 6 endpoints: `search`, `listing`,
`building`, `rent_trends`, `suggestions`, `cities`. Credits: 1 credit each.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s.
See the [Rent.com API
page](https://scavio.dev/rentcom-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/rentcom-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
rc = client.rentcom
res = rc.search("Austin", state="TX", beds=2, price_max=3000)["data"]
print(res["total"], res["average_rent"]["two_bedroom"])
for it in res["listings"][:5]:
    print(it["id"], it["name"], it["price_text"], it["bed_text"], it["deals_text"])
trends = rc.rent_trends("Austin", "TX")["data"]
print(trends["current"]["one_bedroom"]["average_rent"], trends["listing_count"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 100. Neighborhoods and homes -- Trulia local survey, market snapshot, listings

Trulia (trulia.com, Zillow Group's home and neighborhood site): a neighborhood
page with Trulia's local survey (what locals say, safety statements with the
share of residents who agree), resident review counts by topic, amenities,
schools and a market snapshot; homes for sale, for rent or recently sold by
ZIP, city or neighborhood (40 a page, 7 sorts); one home by zpid or one rental
building; one school; and place suggestions. US only, prices in USD;
`language` es on rental searches, buildings and neighborhoods. Brokerage
company names only: no agent names or reviewer names. Namespace `trulia`, 5
endpoints: `neighborhood`, `search`, `property`, `school`, `suggestions`.
Credits: 1 credit each. `credits_used` in the response is what was charged.
The request timeout is raised to at least 240s.
See the [Trulia API
page](https://scavio.dev/trulia-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/trulia-neighborhood?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
tr = client.trulia
hood = tr.neighborhood("85381")["data"]
for s in hood["what_locals_say"]["statements"][:5]:
    print(s["statement"], s["percent"])
print(hood["market"]["snapshot"]["avg_sale_price"]["display"], hood["reviews"]["total"])
homes = tr.search("Austin, TX", beds_min=3, price_max=600000)["data"]
for h in homes["listings"][:5]:
    print(h["zpid"], h["address"], h["price"], h["beds"], h["baths"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 101. New York City real estate -- StreetEasy listings, buildings and market data

StreetEasy (streeteasy.com, Zillow Group's New York City real estate site):
sales, rentals and past sales in an NYC or North NJ area with the price, net
effective rent and months free, beds, baths and the building type; one listing
in full with its price history, monthly charges and open houses (by link, or
by id with `listing_type`); one building and an area's building directory; and
StreetEasy's published monthly market data for NYC (price and rental indexes,
median asking rent, inventory, share of price cuts). Brokerage names only: no
agent personal data. Namespace `streeteasy`, 5 endpoints: `search`, `listing`,
`building`, `buildings`, `market`. Credits: 1 credit each. `credits_used` in
the response is what was charged. The request timeout is raised to at least
240s.
See the [StreetEasy API
page](https://scavio.dev/streeteasy-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/streeteasy-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
se = client.streeteasy
res = se.search("Brooklyn", mode="rent", price_max=4000)["data"]
for it in res["listings"][:5]:
    print(it["id"], it["address"], it["unit"], it["price"], it["beds"], it["net_effective_rent"])
idx = se.market(type="rentals", metric="rental_index")["data"]
for a in idx["areas"]:
    print(a["area"], a["latest"]["month"], a["latest"]["value"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 102. Rentals in the US and Canada -- RentCafe rents, specials, reviews, rent trends

RentCafe (rentcafe.com, Yardi's US and Canada rental listing site): rental
search by location, city or ZIP with the rent range, rating, review count and
rent specials (25 a page; one of beds, rent specials, short-term, furnished,
utilities included or an amenity per search, plus price and pet-friendly); one
listing in full; every unit of a floor plan; resident reviews with RentCafe's
own summary (no names); suggestions; and a US city's rent trends. `market` us
or ca (USD or CAD), `language` en or fr. Namespace `rentcafe`, 6 endpoints:
`search`, `property`, `floorplan_units`, `reviews`, `suggestions`,
`rent_trends`. Credits: 1 credit each. `credits_used` in the response is what
was charged. The request timeout is raised to at least 240s.
See the [RentCafe API
page](https://scavio.dev/rentcafe-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/rentcafe-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
rcf = client.rentcafe
res = rcf.search("austin-tx", price_max=2000)["data"]
for it in res["listings"][:5]:
    print(it["id"], it["name"], it["rent_min"], it["rent_max"], it["rating"], it["rent_specials"])
trends = rcf.rent_trends("Austin", "TX")["data"]
print(trends["average_rent"], trends["yoy_change_pct"], trends["last_updated"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 103. Vacation rentals -- Vrbo nightly prices and stay totals for your dates

Vrbo (vrbo.com, Expedia Group's vacation rental site): vacation rentals for a
place or region id and dates with the nightly price, the stay total, deals,
rating and review count as Vrbo shows them, sorted and filtered by property
type, amenity, house rule, location type, Premier Host and bedrooms (the first
50 results; `partial` flags a 3-result answer); one property in full with
amenities, house rules and the site's default stay price (fetched without
dates); and destination suggestions. 20 market-languages (`market`). No host
names, reviews or calendar. Namespace `vrbo`, 3 endpoints: `search`,
`property`, `suggestions`. Credits: billed on actual cost: `search` 2 credits
per attempt, 2 to 8 (typically 2 to 6); `property` and `suggestions` 2.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 250s.
See the [Vrbo API
page](https://scavio.dev/vrbo-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/vrbo-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
vr = client.vrbo
res = vr.search("2027-01-15", "2027-01-18", destination="Destin, Florida", adults=2)["data"]
print(res["matched_total"], res["count"], res["partial"])
for p in res["properties"][:5]:
    print(p["property_id"], p["price"]["nightly"], p["price"]["total"], p["rating"]["score"])
home = vr.property("1046285")["data"]
print(home["property_type"], home["space"]["bedrooms"], home["default_price"]["price_display"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 104. Car prices -- TrueCar listings, price rating, dealer fees, model overviews

TrueCar (truecar.com, the US car-buying marketplace): new and used dealer
inventory around a ZIP with the price, MSRP, TrueCar's price rating and the
dealer, plus national price and trim stats; one listing by VIN or link with
the price summary and dealer fees (the VIN is input only, never returned, so a
search result cannot feed `listing`); a model overview with trims and starting
prices; owner reviews; a dealer and its inventory; suggestions, makes and
models. US only, prices in USD. Namespace `truecar`, 9 endpoints: `search`,
`listing`, `model`, `reviews`, `dealer`, `dealer_inventory`, `suggestions`,
`makes`, `models`. Credits: 1 credit each. `credits_used` in the response is
what was charged. The request timeout is raised to at least 240s. TrueCar has
no public API.
See the [TrueCar API
page](https://scavio.dev/truecar-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/truecar-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
tc = client.truecar
res = tc.search("10001", make="Toyota", model="RAV4", condition="used")["data"]
for it in res["items"][:5]:
    print(it["year"], it["trim"], it["price"], it["price_rating"], it["mileage"], it["dealer"]["name"])
print(res["national"]["price"])
model = tc.model("Toyota", "RAV4")["data"]
for t in model["trims"]:
    print(t["trim"], t["starting_msrp"], t["starting_market_average"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 105. Car research -- Edmunds deal rating, suggested price per trim, appraisal values

Edmunds (edmunds.com, the US car research and shopping site): new, used and
certified listings around a city and state with the price, Edmunds' deal
rating (local and national) and estimated days to sell; one listing (VIN with
make, model and year, input only); owner reviews of a model year; a dealer
page; a model year's research page; MSRP, invoice and Edmunds Suggested Price
per trim; used-car appraisal values per style and condition; and a make's
models. The suggested price and appraisal name the place Edmunds priced for.
US only, prices in USD; 2 credits per call. Namespace `edmunds`, 8 endpoints:
`search`, `listing`, `reviews`, `dealer`, `model`, `price`, `appraisal`,
`makes`. Credits: 2 credits each. `credits_used` in the response is what was
charged. The request timeout is raised to at least 250s. Edmunds' own API is
for partners and dealers only.
See the [Edmunds API
page](https://scavio.dev/edmunds-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/edmunds-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ed = client.edmunds
res = ed.search("New York", "NY", make="Toyota", model="RAV4")["data"]
for it in res["items"][:5]:
    print(it["year"], it["trim"], it["price"], it["mileage"], it["deal_rating"]["local"]["rating"])
price = ed.price("Toyota", "RAV4", 2025)["data"]
print(price["suggested_price_near"]["text"])
for t in price["trims"]:
    print(t["trim"], t["msrp"], t["invoice"], t["edmunds_suggested"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 106. Car values -- Kelley Blue Book values at a ZIP, listings, owner reviews

Kelley Blue Book (kbb.com, Cox Automotive's car value and research site): a
car's KBB values by make, model, year and trim for buy_used, buy_new or
trade_in_sell (every price type the page gives, 17 for a used car: Fair
Purchase Price, private party, trade-in and auction values per condition),
optionally at a ZIP (not for buy_new); a model year page with its trims; cars
for sale near a ZIP with KBB's fair purchase price; one listing; owner
reviews; dealers near a ZIP and one dealer; and the make and model directory.
US only, prices in USD. Namespace `kbb`, 8 endpoints: `car_value`, `model`,
`search`, `listing`, `reviews`, `dealers`, `dealer`, `makes_models`. Credits:
1 credit each; `car_value` with a `zip` 2 (6 when a second way of reading the
page is needed); `reviews` beyond page 1, with a sort other than recent or a
star filter up to 5. `credits_used` in the response is what was charged. The
request timeout is raised to at least 250s. KBB's own data feed is a business
contract, not a self-serve API.
See the [Kelley Blue Book API
page](https://scavio.dev/kbb-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/kbb-car-value?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
kbb = client.kbb
val = kbb.car_value("Toyota", "rav4", 2021, "le-sport-utility-4d", mileage=40000, zip="10001")
val = val["data"]
print(val["location"]["valid_text"], val["headline"]["fair_purchase_price"]["value"])
for p in val["prices"][:5]:
    print(p["type"], p["value"], p["range_low"], p["range_high"])
cars = kbb.search("10001", make="Toyota", model="RAV4")["data"]
for c in cars["listings"][:5]:
    print(c["title"], c["price"], c["deal_label"], c["kbb_fair_purchase_price"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 107. US homes -- Movoto listings, sold prices and market trends by city or ZIP

Movoto (movoto.com, the US home search site owned by Lower): homes for sale,
sold or for rent by city and state, ZIP, county, neighborhood or school zone
(50 a page, with Movoto's market summary, snapshot and top ZIP codes and
neighborhoods); one home in full with its features, price history and schools;
a city's or ZIP code's market trends (median list price, price per square
foot, days on market, inventory, by home type); search-box suggestions; and
one school page. US only, prices in USD. No listing-agent names or contact
details are returned; brokerage company names are. Namespace `movoto`, 5
endpoints: `search`, `property`, `market_trends`, `suggestions`, `school`.
Credits: 1 credit each. `credits_used` in the response is what was charged.
The request timeout is raised to at least 240s.
See the [Movoto API
page](https://scavio.dev/movoto-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/movoto-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
mv = client.movoto
res = mv.search("Austin", state="TX")["data"]
print(res["total"], res["pages"])
for home in res["listings"][:5]:
    print(home["address"]["full"], home["price"], home["beds"], home["baths"], home["sqft"])
trends = mv.market_trends("Los Angeles", state="CA")["data"]
print(trends["summary"])
for card in trends["stat_cards"]:
    print(card["title"], card["value"], card["change"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 108. US rentals -- HotPads rents, rent history and move-in costs and fees

HotPads (hotpads.com, Zillow Group's rental search site): rentals in an area
(apartments, houses, rooms, by-owner and more) grouped by building with the
rent range, beds, baths, square feet and special offers, filtered and sorted;
one listing or building in full with floor plans, office hours, amenities and
pet policies; a listing's rent history; its move-in and monthly costs and
fees; and area suggestions. US only, rents in USD. No landlord names or phone
numbers are returned. Namespace `hotpads`, 5 endpoints: `search`, `listing`,
`price_history`, `fees`, `suggestions`. Credits: 1 credit each. `credits_used`
in the response is what was charged. The request timeout is raised to at least
240s.
See the [HotPads API
page](https://scavio.dev/hotpads-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/hotpads-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
hp = client.hotpads
res = hp.search("brooklyn-new-york-ny", beds=1, sort="price_low")["data"]
print(res["title"], res["total_units"], res["min_price"])
for building in res["buildings"][:5]:
    for it in building["listings"]:
        print(it["title"], it["price_min"], it["price_max"], it["address"]["street"])
fees = hp.fees("24ga0pwypzg8y")["data"]
print(fees["base_rent"]["min"], fees["monthly_total"]["min"], fees["move_in_total"]["min"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 109. US rentals -- Apartment List rents, rent specials and the rent report

Apartment List (apartmentlist.com, the US rental search site): rentals in a
city, neighborhood or ZIP code with the rent range and rent per bed count,
units available, the soonest move-in date and rent specials (20 a page,
filtered and sorted); one listing with every floor plan and unit price;
Apartment List's published rent report for a city (median rents, month and
year growth, the metro table); a place's market summary; review summaries for
a city's listings; and place suggestions. US only, rents in USD. Namespace
`apartmentlist`, 6 endpoints: `suggestions`, `search`, `listing`,
`rent_report`, `market_summary`, `review_summaries`. Credits: 1 credit each.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s.
See the [Apartment List API
page](https://scavio.dev/apartmentlist-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/apartmentlist-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
al = client.apartmentlist
res = al.search(city="Austin", state="TX")["data"]
print(res["total_listings"], res["total_units"], res["pages"])
for it in res["listings"][:5]:
    print(it["name"], it["price_min"], it["price_max"], it["units_available"], it["has_rent_special"])
report = al.rent_report(city="Chicago", state="IL")["data"]
glance = report["at_a_glance"]
print(glance["median_rent_1br"], glance["median_rent_2br"], glance["rent_growth_year"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 110. Homes for sale and rent -- Compass listings, pricing and price history

Compass (compass.com, the US real estate brokerage): homes for sale, for rent
or sold in an area with the price, beds, baths, square feet, status and open
houses, filtered and sorted; one listing in full with pricing (monthly
charges, financing terms), dates, price history, key details, schools and the
building; and place suggestions. US, prices in USD; 2 credits per call.
Brokerage names only, never agent names. Namespace `compass`, 3 endpoints:
`search`, `listing`, `suggestions`. Credits: 2 credits each. `credits_used` in
the response is what was charged. The request timeout is raised to at least
240s.
See the [Compass API
page](https://scavio.dev/compass-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/compass-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
cp = client.compass
res = cp.search("manhattan-ny", mode="for_sale", beds_min=2, price_max=2000000)["data"]
print(res["total"], res["reachable"], res["pages"])
for it in res["listings"][:5]:
    print(it["address"], it["price_text"], it["beds"], it["baths"], it["status"])
home = cp.listing(res["listings"][0]["url"])["data"]
print(home["pricing"]["price"], home["pricing"]["monthly_charges"], home["days_on_market"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 111. Affordable housing -- Section 8 rentals, waiting lists, housing authorities

AffordableHousing.com (affordablehousing.com, the US affordable and Section 8
rental site): rentals in a state, city, county or ZIP code with the rent
range, beds, baths, Section 8 acceptance and income restrictions, filtered by
price, pets, utilities, age and accessibility; one listing in full; place
suggestions; open and opening-soon Section 8 and public housing waiting lists;
one housing authority (public housing agency) with its waitlist status; and a
state's housing authorities. US only, rents in USD. The agency's public phone
number is returned, never a landlord's contact details. Namespace
`affordablehousing`, 6 endpoints: `search`, `listing`, `suggestions`,
`waiting_lists`, `housing_authority`, `housing_authorities`. Credits: `search`
and `suggestions` 2 credits, the other endpoints 1. `credits_used` in the
response is what was charged. The request timeout is raised to at least 240s.
See the [AffordableHousing.com API
page](https://scavio.dev/affordablehousing-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/affordablehousing-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ah = client.affordablehousing
res = ah.search("TX", city="Houston", sort="price_asc")["data"]
print(res["total"], res["pages"])
for it in res["listings"][:5]:
    print(it["title"], it["rent_min"], it["rent_max"], it["beds_min"], it["section8_accepted"])
pha = ah.housing_authorities("CA")["data"]
for agency in pha["agencies"][:5]:
    print(agency["name"], agency["waitlist_status"], agency["jurisdiction"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 112. New homes -- Lennar homesites, plans, communities, promotions and payments

Lennar (lennar.com, the US homebuilder): new homes, homesites, plans and
communities in a market, state, city, point or map box with the price, was
price, beds, baths and square feet, filtered by home type, availability,
features and schools; one community with its plans, homesites, HOA fee and tax
rate; one plan; one homesite; a master-planned community; every market and one
market's cities and filter codes; suggestions; a link resolved to its record;
a market's current promotions; and a monthly payment estimate for a homesite.
US only, prices in USD. For new-home price tracking, incentive monitoring and
market comparisons. Namespace `lennar`, 11 endpoints: `search`, `community`,
`plan`, `home`, `master_planned`, `markets`, `market`, `suggestions`,
`resolve`, `promotions`, `payment`. Credits: 1 credit each. `credits_used` in
the response is what was charged. The request timeout is raised to at least
240s.
See the [Lennar API
page](https://scavio.dev/lennar-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/lennar-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ln = client.lennar
res = ln.search("DAL", sort="price_asc")["data"]
print(res["total"], res["count"])
for home in res["homes"][:5]:
    print(home["address"], home["price"], home["was_price"], home["beds"], home["sqft"])
com = ln.community("22704")["data"]
print(com["name"], com["base_price"], com["hoa_fee"], com["tax_rate_percent"])
for plan in com["plans"][:3]:
    print(plan["name"], plan["starting_price"], plan["available_homesites"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 113. Self storage -- Extra Space Storage unit prices and city storage prices

Extra Space Storage (extraspace.com, the US self-storage REIT): self-storage
facilities near a ZIP code, city, place or point (up to 120, nearest first)
with the starting price by unit size, promotions, rating and features,
filtered by climate control, drive-up, indoor, vehicle storage, 24-hour access
and unit size; one facility with every unit and its price; a facility's
reviews (no reviewer names); a city's published storage prices by unit size;
and Extra Space's locations by state. US only, prices in USD. Namespace
`extraspace`, 5 endpoints: `search`, `facility`, `reviews`, `city_prices`,
`locations`. Credits: 1 credit each. `credits_used` in the response is what
was charged. The request timeout is raised to at least 240s.
See the [Extra Space Storage API
page](https://scavio.dev/extraspace-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/extraspace-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
es = client.extraspace
res = es.search("90012")["data"]
print(res["total"], res["count"])
for f in res["facilities"][:5]:
    print(f["name"], f["distance_mi"], f["starting_at"]["small"], f["starting_at"]["large"])
city = es.city_prices("Dallas", "TX")["data"]
for row in city["price_stats"][1:5]:
    print(row["category"], row["store_count"], row["lowest"], row["average"], row["highest"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 114. Self storage -- Public Storage unit prices in the US and Canada

Public Storage (publicstorage.com, the US self-storage operator, also in
Canada): self-storage facilities near a place with the starting price,
distance, hours and features, filtered by climate control, drive-up, 24/7
access, business, vehicle, RV and boat storage and unit size; one facility
with every unit's online price, in-store rent, promotion and move-in cost; and
a US facility's reviews (no reviewer names). `market` us or ca (USD or CAD),
`language` en or fr in Canada. Namespace `publicstorage`, 3 endpoints:
`search`, `facility`, `reviews`. Credits: 1 credit each. `credits_used` in the
response is what was charged. The request timeout is raised to at least 240s.
See the [Public Storage API
page](https://scavio.dev/publicstorage-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/publicstorage-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ps = client.publicstorage
res = ps.search("75201", sort="price_low")["data"]
for f in res["facilities"][:5]:
    print(f["name"], f["distance"], f["starting_from"], f["currency"])
fac = ps.facility("2044")["data"]
for unit in fac["units"][:5]:
    print(unit["name"], unit["online_price"], unit["in_store_rent"], unit["move_in_cost"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 115. Estate sales -- EstateSales.net sales near a ZIP, companies and items

EstateSales.net (estatesales.net, the US estate sale directory): estate sales,
auctions and moving sales near a ZIP code or city with the dates, sale type,
picture count and the company running it; one sale in full with every date,
terms, description and pictures; a metro's estate sale companies and one
company's profile and sales; keyword search over sales and marketplace items;
and one marketplace item with its price, bids and shipping. US only, prices in
USD. A private sale gives its city, state and ZIP only; a company's contact
details are public business data. Namespace `estatesales`, 6 endpoints:
`sales`, `sale`, `companies`, `company`, `search`, `item`. Credits: 1 credit
each. `credits_used` in the response is what was charged. The request timeout
is raised to at least 240s.
See the [EstateSales.net API
page](https://scavio.dev/estatesales-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/estatesales-sales?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ess = client.estatesales
res = ess.sales("75201")["data"]
print(res["total_count"], res["count"])
for sale in res["sales"][:5]:
    print(sale["name"], sale["type_name"], sale["city"], sale["starts_at_local"], sale["picture_count"])
sale = ess.sale("5114622")["data"]
print(sale["name"], sale["location"]["city"], sale["picture_count"])
for day in sale["dates"]:
    print(day["starts_at_local"], day["ends_at_local"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 116. Books -- Goodreads ratings, reviews, authors, series, lists and quotes

Goodreads (goodreads.com, Amazon's book community): book, author, quote and
list search; one book with its rating, rating distribution, genres, series,
editions and awards; reader reviews with Goodreads' own sort and star,
language and edition filters (no reviewer names); suggestions; an author and
their books; a series; a work's editions; a Listopia list, a book's lists and
list search; quotes; a genre page; and new releases by genre or month. One
global English site. Namespace `goodreads`, 14 endpoints: `search`, `book`,
`reviews`, `suggestions`, `author`, `author_books`, `series`, `editions`,
`list`, `book_lists`, `list_search`, `quotes`, `genre`, `new_releases`.
Credits: 1 credit each. `credits_used` in the response is what was charged.
The request timeout is raised to at least 240s. Goodreads retired its official
API (no new developer keys since 2020).
See the [Goodreads API
page](https://scavio.dev/goodreads-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/goodreads-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
gr = client.goodreads
res = gr.search("dune")["data"]
for b in res["results"][:5]:
    print(b["book_id"], b["title"], b["rating"], b["ratings_count"], b["published"])
book = gr.book("44767458")["data"]
print(book["title"], book["rating"], book["ratings_count"], book["reviews_count"])
print([g["name"] for g in book["genres"][:3]])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 117. Hotels -- Expedia prices for your dates and price calendars in 51 markets

Expedia (expedia.com, Expedia Group's travel booking site): hotels and stays
for a place or region id and dates with the nightly price, the stay total, the
was price, rating and review count, sorted and filtered by star rating,
amenity and guest rating (the top results of Expedia's first page; `partial`
flags a 3-result answer); one property in full with amenities, fees, policies
and Expedia's own summary lines (fetched without dates); a property's price
calendar for every day Expedia shows; and destination suggestions. 51
market-languages (`market`), each in its own language and currency. No
reviews, dated room rates or flights. Namespace `expedia`, 4 endpoints:
`search`, `property`, `price_calendar`, `suggestions`. Credits: billed on
actual cost: 2 credits per call (1 on some New Zealand, Korea and Indonesia
pages). `credits_used` in the response is what was charged. The request
timeout is raised to at least 250s.
See the [Expedia API
page](https://scavio.dev/expedia-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/expedia-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ex = client.expedia
res = ex.search("2027-01-25", "2027-01-28", destination="Las Vegas, NV", adults=2)["data"]
print(res["destination_name"], res["matched_total"], res["count"], res["partial"])
for p in res["properties"]:
    print(p["property_id"], p["name"], p["price"]["nightly"], p["price"]["total"], p["rating"]["score"])
hotel = ex.property("17117062")["data"]
print(hotel["name"], hotel["stars"], hotel["rating"]["score"], hotel["fees"][:2])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 118. Sporting goods -- Academy Sports + Outdoors prices, deals and units per store

Academy Sports + Outdoors (academy.com, the US sporting goods retailer):
keyword search, category and deal listings (Hot Deals, Clearance, Black
Friday, the Flash Sale) with the price, was price, saving and Academy's deal
tags, sorted and filtered by any facet; one product in full with every
variant; the exact units one store holds for pickup per variant; stores near a
ZIP or a point and store details with hours; the category tree; and search
suggestions. US only, prices in USD and national (the same at every store).
Product types are described as Academy lists them. Namespace `academy`, 9
endpoints: `search`, `product`, `store_availability`, `stores`, `store`,
`category`, `categories`, `deals`, `suggestions`. Credits: 1 credit each.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s.
See the [Academy Sports + Outdoors API
page](https://scavio.dev/academy-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/academy-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ac = client.academy
res = ac.search("yeti tumbler")["data"]
print(res["total"], res["total_pages"])
for it in res["items"][:5]:
    print(it["name"], it["price"], it["was_price"], it["percent_off"])
stock = ac.store_availability("111805768", "19", "TX")["data"]
print(stock["in_store_units_total"], stock["variants_in_stock_at_store"])
for v in stock["variants"][:5]:
    print(v["sku_id"], v["store_status"], v["in_store_units"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 119. Body care and candles -- Bath & Body Works prices, offers and store pickup

Bath & Body Works (bathandbodyworks.com, the US body care and home fragrance
retailer, and bathandbodyworks.ca): keyword search and category listings (48
results, as the site shows them) with the price, list price, promotions,
fragrance and size; the category tree; one product in full; a product's
promotions with their start and end times; the current offers; whether one
store takes a pickup order for a product and the most it lets you reserve; the
store directory and one store; and a product's rating with its newest reviews.
Country us or ca, prices in USD or CAD. Namespace `bathandbodyworks`, 10
endpoints: `search`, `category`, `categories`, `product`, `promotions`,
`offers`, `store_availability`, `store`, `stores`, `reviews_summary`. Credits:
1 credit each. `credits_used` in the response is what was charged. The request
timeout is raised to at least 240s.
See the [Bath & Body Works API
page](https://scavio.dev/bathandbodyworks-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/bathandbodyworks-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
bbw = client.bathandbodyworks
res = bbw.search("candle", sort="top_rated")["data"]
print(res["total"], res["count"], res["currency"])
for it in res["products"][:5]:
    print(it["name"], it["size"], it["price"], [p["callout"] for p in it["promotions"]])
pickup = bbw.store_availability("BBW00010", product_id="028029548")["data"]
print(pickup["store"]["name"], pickup["store_orderable"], pickup["pickup_purchase_limit"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 120. Apparel -- Gap, Old Navy, Banana Republic and Athleta prices and store stock

Gap Inc. (gap.com): one API for Gap, Old Navy, Banana Republic, Athleta, Gap
Factory and Banana Republic Factory (brand). Keyword search and category
listings with the regular price, the price shown and whether it is a promotion
or a markdown; the category tree; one product with every color and size;
prices for up to 100 colors in one call; stores near a ZIP, a postal code or a
point and one store with hours; the in, low or out pickup stock of sizes at up
to 10 stores; search suggestions, trending searches and the deal pages.
Country us or ca (English or French), prices in USD or CAD. A checkout code is
never applied to a price. Namespace `gap`, 11 endpoints: `search`, `category`,
`categories`, `product`, `prices`, `stores`, `store`, `store_stock`,
`suggestions`, `trending`, `deals`. Credits: 1 credit each. `credits_used` in
the response is what was charged. The request timeout is raised to at least
240s.
See the [Gap Inc. API
page](https://scavio.dev/gap-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/gap-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
gap = client.gap
res = gap.search("jeans", brand="gap")["data"]
print(res["brand_name"], res["total"], res["pages"])
for it in res["items"][:5]:
    print(it["name"], it["regular_price"], it["effective_price"], it["price_type"])
stock = gap.store_stock(["220", "1519", "1456"], sku_ids=["4035400023503"])["data"]
for sku in stock["skus"]:
    print(sku["sku_id"], [(s["store_id"], s["status"]) for s in sku["stores"]])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 121. Cashback -- Rakuten cash back rates, coupons and deals in the US, UK and Canada

Rakuten (rakuten.com, the cashback site formerly Ebates; rakuten.co.uk and
rakuten.ca too): the store directory with each store's cash back rate and was
rate, one store with its rate, terms and coupons, a store's coupons, a rate
check for up to 100 stores in one call, search over stores, coupons and
products, search suggestions, a category of stores, the event deal pages
(Black Friday, Cyber Monday, the coupons hub) and the card-linked in-store
offers. Country us, gb or ca (English or French). Rates are as Rakuten writes
them; Rakuten gives no rate end dates, and its shopping-trip links are never
returned. Namespace `rakuten`, 9 endpoints: `stores`, `store`,
`store_coupons`, `rates`, `search`, `suggestions`, `category`, `deals`,
`in_store`. Credits: 1 credit each. `credits_used` in the response is what was
charged. The request timeout is raised to at least 240s.
See the [Rakuten API
page](https://scavio.dev/rakuten-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/rakuten-stores?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
rk = client.rakuten
res = rk.stores(sort="cashback")["data"]
print(res["total"], res["pages"])
for st in res["stores"][:5]:
    print(st["name"], st["rate_text"], st["was_text"], st["elevated"])
rates = rk.rates(["8333", "7206", "3930", "9528"])["data"]
for st in rates["stores"]:
    print(st["name"], st["rate_text"], st["amount"], st["type"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 122. Warehouse club -- BJ's Wholesale Club prices, coupons, reviews and clubs

BJ's Wholesale Club (bjs.com, the US warehouse club): one product in full,
keyword search and category listings (40 results, as the page lists them) with
the online price, sale dates and whether an item is in stock online or in
club, the category tree, product reviews, the guest coupon book and the club
directory by state. Where BJ's shows a member-only price to a visitor, the
answer flags it and gives the list price only; a club-only item has no online
price. Search is priced for the club BJ's assigns to the visit: a club cannot
be chosen, and there is no club price, club stock or ZIP club finder. US only,
prices in USD. Namespace `bjs`, 7 endpoints: `product`, `search`, `category`,
`categories`, `reviews`, `coupons`, `clubs`. Credits: 1 credit each.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s.
See the [BJ's Wholesale Club API
page](https://scavio.dev/bjs-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/bjs-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
bjs = client.bjs
res = bjs.search("coffee")["data"]
print(res["total"], res["count"], res["priced_for"])
for it in res["results"][:5]:
    print(it["name"], it["price"], it["member_only_price"], it["club_only"])
clubs = bjs.clubs(state="NY")["data"]
for club in clubs["clubs"][:5]:
    print(club["club_id"], club["name"], club["state"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 123. Shoes -- Zappos and 6pm prices and exact units per size, width and color

Zappos (zappos.com, the US shoe and clothing store) and 6pm (6pm.com, its
outlet site; site): keyword search or a catalog browse by facets, sorted, with
the price, original price, percent off and units on hand; one product with
every color and size and the exact warehouse units per size, width and color;
customer reviews with comfort, look and fit ratings; customer questions; the
lowest price of each color as Zappos gives it; category facets; and search
suggestions. Reviews, questions and lowest prices come from zappos.com. US
only, prices in USD; no stores. No reviewer names. Namespace `zappos`, 7
endpoints: `search`, `product`, `reviews`, `questions`, `lowest_prices`,
`categories`, `suggestions`. Credits: 1 credit each. `credits_used` in the
response is what was charged. The request timeout is raised to at least 240s.
See the [Zappos API
page](https://scavio.dev/zappos-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/zappos-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
zp = client.zappos
res = zp.search(query="running shoes")["data"]
print(res["total"], res["total_pages"])
for it in res["items"][:5]:
    print(it["brand"], it["name"], it["price"], it["original_price"], it["on_hand"])
shoe = zp.product("10002909")["data"]
print(shoe["name"], shoe["total_on_hand"], shoe["in_stock_sku_count"])
for style in shoe["styles"][:3]:
    print(style["color"], style["price"], [(s["size"], s["width"], s["on_hand"]) for s in style["skus"][:4]])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 124. Computers and electronics -- Newegg prices, seller offers, reviews and deals

Newegg (newegg.com, the US computer and electronics store): keyword search,
category listings and the deal stores (Shell Shocker, Black Friday) with the
price, list price, instant rebate, shipping and the seller; the category menu;
one item in full; every seller's offer on an item by condition; reviews; a
marketplace seller's store and its products; and search suggestions. Country
us, ca or one of 9 Newegg Global storefronts (local currency, part of the
catalog). When Newegg serves a different item than the one requested, the
answer shows both. Namespace `newegg`, 10 endpoints: `search`, `category`,
`categories`, `product`, `offers`, `reviews`, `deals`, `seller`,
`seller_products`, `suggestions`. Credits: 2 credits each. `credits_used` in
the response is what was charged. The request timeout is raised to at least
240s.
See the [Newegg API
page](https://scavio.dev/newegg-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/newegg-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ne = client.newegg
res = ne.search("rtx 5070")["data"]
print(res["total"], res["count"])
for it in res["items"][:5]:
    print(it["title"], it["price"], it["list_price"], it["in_stock"])
offers = ne.offers("19-113-877", sort="price")["data"]
print(offers["total"], [(t["condition"], t["lowest_price"]) for t in offers["tabs"]])
for o in offers["offers"][:5]:
    print(o["price"], o["condition"], o["shipping"]["free"], o["seller"]["marketplace"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 125. Outdoor gear -- REI prices, deals, reviews and store pickup status

REI (rei.com, the US outdoor co-op): keyword search, category listings and the
deal pages (sale and clearance, REI Outlet) with the price, regular price,
percent off and flags, sorted and filtered by facets or one store; one product
in full with every SKU; reviews; the pickup status of one SKU at the REI
stores near a ZIP, a city or a point (in stock, ship to store or unavailable:
REI publishes no unit counts); stores and one store with hours; and search
suggestions. US only, prices in USD as shown to a visitor who is not signed
in; no used gear online and no member prices. Namespace `rei`, 9 endpoints:
`search`, `category`, `deals`, `product`, `reviews`, `store_stock`, `stores`,
`store`, `suggestions`. Credits: 2 credits each. `credits_used` in the
response is what was charged. The request timeout is raised to at least 240s.
See the [REI API
page](https://scavio.dev/rei-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/rei-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
rei = client.rei
res = rei.search("rain jacket")["data"]
print(res["total"], res["total_pages"])
for it in res["items"][:5]:
    print(it["brand"], it["name"], it["price"], it["regular_price"], it["sale"])
stock = rei.store_stock("2437020001", zip="98101")["data"]
print(stock["in_stock_count"], stock["ship_to_store_count"])
for row in stock["stores"][:5]:
    print(row["store"]["name"], row["status"], row["estimated_arrival"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 126. Video shopping -- QVC and HSN prices, today's special, program guide and reviews

QVC (qvc.com, qvcuk.com, qvc.de, qvc.it, qvc.jp) and HSN (hsn.com), the video
shopping networks (site): keyword search with the price, QVC's everyday price,
the special price (Today's Special Value, Black Friday Sale), easy pay, rating
and stock; one product in full and up to 20 products in one call; today's
special with its start and end times; what is on air now; the program guide by
day and channel; the items HSN presented in one show hour; a qvc.com category
or collection; search suggestions; and the first page of a product's reviews
and questions as the product page shows it (no paging, no reviewer names). QVC
market us, uk, de, it or jp in its own language and currency; HSN US only.
Show names are kept as given; host and guest names are not included. Namespace
`qvc`, 10 endpoints: `search`, `product`, `products`, `todays_special`,
`on_air`, `program_guide`, `recently_aired`, `category`, `suggestions`,
`reviews`. Credits: 1 credit each. `credits_used` in the response is what was
charged. The request timeout is raised to at least 240s.
See the [QVC + HSN API
page](https://scavio.dev/qvc-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/qvc-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
qvc = client.qvc
res = qvc.search("blender")["data"]
print(res["total"], res["total_pages"], res["currency"])
for it in res["items"][:5]:
    print(it["title"], it["price"], it["qvc_price"], it["special_price"], it["stock"])
tsv = qvc.todays_special()["data"]
print(tsv["headline"], tsv["window"]["starts_at"], tsv["window"]["ends_at"])
print(tsv["item"]["title"], tsv["item"]["price"], tsv["item"]["qvc_price"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 127. Books -- Barnes & Noble prices, formats, bestsellers and store pickup

Barnes & Noble (barnesandnoble.com, the US bookseller): keyword search and
collection listings (24 results, as the site shows them) with the format,
price, original price, sale flag, sales rank and rating, sorted and filtered
by the site's own filters; one title by EAN or ISBN with every format the page
links and a short overview excerpt; store pickup flags for a title at the
stores near a ZIP, a city or a store (eligible and available, no unit counts);
stores near a place or a point and one store with hours; search suggestions;
the bestseller lists; the category menu; and the deal pages. Member offers are
given as the page's offer text, never a member price. US only, prices in USD.
Namespace `barnesandnoble`, 10 endpoints: `search`, `product`,
`store_availability`, `stores`, `store`, `suggestions`, `bestsellers`,
`category`, `categories`, `deals`. Credits: 1 credit each. `credits_used` in
the response is what was charged. The request timeout is raised to at least
240s.
See the [Barnes & Noble API
page](https://scavio.dev/barnesandnoble-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/barnesandnoble-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
bn = client.barnesandnoble
res = bn.search("project hail mary")["data"]
print(res["total"], res["count"])
for it in res["items"][:5]:
    print(it["title"], it["format"], it["price"], it["original_price"], it["on_sale"])
pickup = bn.store_availability("60611", ean="9780439023528")["data"]
print(pickup["count"], pickup["available_count"])
for st in pickup["stores"][:5]:
    print(st["name"], st["distance_miles"], st["eligible"], st["available"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 128. Used books -- ThriftBooks prices per format and condition, editions and copies

ThriftBooks (thriftbooks.com, the US online used-book seller): keyword search
or a catalog browse with the bestseller, deals and new release lists, filtered
by format, condition, language, genre and price; an ISBN lookup with the price
of every format and condition; a work's format x condition table with the
price, list price and quantity of each condition (a New quantity of 500 means
500 or more); one edition with a short overview excerpt; every copy for sale
of an edition; all editions of a work; customer reviews; and search
suggestions. US storefront, prices in USD as a visitor who is not signed in
sees them. Namespace `thriftbooks`, 8 endpoints: `search`, `isbn`, `work`,
`edition`, `copies`, `editions`, `reviews`, `suggestions`. Credits: 1 credit
each. `credits_used` in the response is what was charged. The request timeout
is raised to at least 240s.
See the [ThriftBooks API
page](https://scavio.dev/thriftbooks-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/thriftbooks-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
tb = client.thriftbooks
book = tb.isbn("9780593135204")["data"]
print(book["work_id"], book["low_price"], book["high_price"])
table = tb.work(book["work_id"])["data"]
for fmt in table["formats"]:
    print(fmt["format"], [(c["condition"], c["price"], c["quantity"]) for c in fmt["conditions"]])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 129. Moving and storage -- U-Haul truck rental rates, locations and self-storage

U-Haul (uhaul.com, the US and Canada truck rental and self-storage company):
U-Haul's own truck rental rates for a one-way or in-town move on a date, from
U-Haul's public quote form (nothing is reserved, and the quote names no pickup
location); U-Haul locations near a place by service; one location;
self-storage facilities near a place with the starting rate, rating and
features, and one facility; customer reviews of a location or facility; place
suggestions; and moving supplies prices in USD or CAD. US and Canada, on
U-Haul's English, Spanish or French site. Namespace `uhaul`, 8 endpoints:
`truck_quote`, `locations`, `location`, `storage_search`, `storage_facility`,
`reviews`, `suggestions`, `supplies`. Credits: 1 credit each. `credits_used`
in the response is what was charged. The request timeout is raised to at least
240s.
See the [U-Haul API
page](https://scavio.dev/uhaul-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/uhaul-truck-quote?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
uh = client.uhaul
quote = uh.truck_quote("Dallas, TX", "2026-12-11", dropoff="Austin, TX")["data"]
print(quote["move_type"], quote["allowed_miles"], quote["available_count"])
for t in quote["trucks"]:
    print(t["name"], t["available"], t["rate"], t["rate_kind"])
storage = uh.storage_search("Phoenix, AZ 85004", sort="price")["data"]
for f in storage["facilities"][:5]:
    print(f["name"], f["distance_text"], f["starting_rate"], f["rating"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 130. Home and kitchen -- Williams Sonoma, Pottery Barn and West Elm prices, stock and stores

Williams-Sonoma, Inc. brands (Williams Sonoma, Pottery Barn, Pottery Barn
Kids, Pottery Barn Teen, West Elm, Rejuvenation and Mark and Graham; brand):
one product in full with every SKU, its price, regular price and stock state
(us, and ca for Williams Sonoma, Pottery Barn and West Elm in CAD); the fabric
configurator of a configured piece; standard delivery dates to a ZIP; online
stock ranges per SKU; store pickup per SKU at up to 10 stores; the brands'
stores near a ZIP or a point; the stores showing a product as a floor sample;
the category tree and one category listing; keyword search (page 1, 20
products); the day's popular searches; and Williams Sonoma customer reviews.
West Elm US search is not served. Namespace `williamssonoma`, 12 endpoints:
`product`, `configurator`, `delivery_estimate`, `stock`, `store_pickup`,
`stores`, `floor_samples`, `categories`, `category`, `search`,
`popular_searches`, `reviews`. Credits: 1 credit each, 5 for `search` and
`category`. `credits_used` in the response is what was charged. The request
timeout is raised to at least 240s.
See the [Williams-Sonoma API
page](https://scavio.dev/williamssonoma-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/williamssonoma-product?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ws = client.williamssonoma
item = ws.product("wusthof-classic-chefs-knife", brand="williams_sonoma")["data"]
print(item["name"], item["price"]["min"], item["price"]["regular_min"], item["on_sale"])
for sku in item["skus"][:5]:
    print(sku["sku"], sku["name"], sku["price"], sku["regular_price"], sku["stock"])
pickup = ws.store_pickup("williams_sonoma", ["1468824", "2600435"], ["ST:0859", "ST:6016"])["data"]
for sku in pickup["skus"]:
    print(sku["sku"], [(s["pickup_location_code"], s["available_for_pickup"]) for s in sku["stores"]])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 131. Department store -- Belk prices, coupons, deals and exact store units

Belk (belk.com, the US Southern department store): keyword search, category
and deal listings (Doorbusters, Super Buys, Clearance, Sale Items, Today's
Offers; 60 items a page) with the original and sale price, Belk Rewards+ tier
prices and coupons as belk.com shows them to logged-out visitors (each
labeled, with Belk's own price with the code, never computed); the category
tree; one product with its variants; one variant with its price and stock
flag, optionally every colour at that size; exact store units for up to 5
variants at up to 10 stores; stores near a ZIP and one store with hours; and
the 8 newest reviews as Belk shows them (no reviewer names). US only, prices
in USD. Namespace `belk`, 10 endpoints: `search`, `category`, `deals`,
`categories`, `product`, `variant`, `store_availability`, `stores`, `store`,
`reviews`. Credits: 2 credits each; `product` 2 by Belk's canonical link and 4
when Belk redirects to it (a `product_id` always does), `variant` 4 with
`include_color_prices`, `store_availability` 1 plus 2 per variant whose orin
is looked up. `credits_used` in the response is what was charged. The request
timeout is raised to at least 240s.
See the [Belk API
page](https://scavio.dev/belk-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/belk-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
belk = client.belk
res = belk.search("sweater")["data"]
print(res["total"], res["total_pages"], res["currency"])
for it in res["items"][:5]:
    print(it["title"], it["original_price"]["min"], it["sale_price"]["min"], it["is_doorbuster"])
stock = belk.store_availability(["234", "345", "497"], variant_id="0480063873511")["data"]
for v in stock["variants"]:
    print(v["variant_id"], v["sale_price"], [(s["store_id"], s["units"], s["status"]) for s in v["stores"]])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 132. Apparel -- Abercrombie & Fitch and Hollister prices by storefront and exact store units

Abercrombie & Fitch Co. (abercrombie.com: Abercrombie & Fitch, abercrombie
kids, YPB; hollisterco.com: Hollister, Gilly Hicks; brand anf or hol): keyword
search and category listings (48 products a page, 6 sorts, facets) with the
price, was price and discount text, the member price the site shows publicly
with its own label, and the colors; one product with every color and SKU;
exact units per SKU at the stores near a US ZIP or a point; stores and one
store with this week's hours; the category tree; the current promotions;
product reviews; and search suggestions. 16 storefronts (us, ca, uk, eu, Hong
Kong, Japan, worldwide; several in a second language) in their own currency;
on the worldwide storefronts prices are the site's conversion from USD, with
the USD price alongside. Namespace `abercrombie`, 10 endpoints: `search`,
`product`, `store_stock`, `stores`, `store`, `category`, `categories`,
`promotions`, `reviews`, `suggestions`. Credits: 1 credit each; `reviews` 2
without the product `url`. `credits_used` in the response is what was charged.
The request timeout is raised to at least 240s.
See the [Abercrombie & Fitch API
page](https://scavio.dev/abercrombie-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/abercrombie-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
anf = client.abercrombie
res = anf.search("baggy jeans", brand="anf")["data"]
print(res["brand_name"], res["total"], res["currency"])
for p in res["products"][:5]:
    print(p["name"], p["price"]["current"], p["price"]["original"], p["price"]["flag"])
stock = anf.store_stock(["662258406", "662258414"], zip="10001")["data"]
for st in stock["stores"][:5]:
    print(st["name"], st["distance"], [(s["sku"], s["units"], s["status"]) for s in st["stock"]])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 133. Outdoor apparel -- L.L.Bean prices in the US, Canada and 12 countries, store units and reviews

L.L.Bean (llbean.com, the US outdoor apparel and gear retailer): keyword
search, category and deal listings (48 a page, 6 sorts, facets) with the
price, full price, sale price and stock; the department tree; one product with
every item, color and size; exact store units per SKU at up to 20 stores or
all of them; stores near a ZIP, a point or a city; written reviews with fit
data (4 sorts, up to 100 a page, no reviewer names) and the review summary; a
delivery estimate to a ZIP; and search suggestions. Catalog markets us (USD),
ca (CAD) and intl (12 countries in local currency); stores, reviews and
delivery estimates are US. Prices as shown to a visitor who is not signed in,
never a member, Rewards or card price. Namespace `llbean`, 11 endpoints:
`search`, `category`, `categories`, `product`, `store_stock`, `stores`,
`reviews`, `review_summary`, `delivery_estimate`, `suggestions`, `deals`.
Credits: 1 credit each. `credits_used` in the response is what was charged.
The request timeout is raised to at least 240s.
See the [L.L.Bean API
page](https://scavio.dev/llbean-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/llbean-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
lb = client.llbean
res = lb.search("fleece jacket")["data"]
print(res["total"], res["total_pages"], res["currency"])
for it in res["items"][:5]:
    print(it["name"], it["price"], it["full_price"], it["sale_price"], it["stock"])
stock = lb.store_stock("112644", product_id="37037", store_ids=["0040", "1350", "2140"])["data"]
for st in stock["stores"]:
    print(st["store_id"], st["units"], st["skus_in_stock"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 134. Music gear -- Sweetwater prices, units on hand, serial-numbered units and deals

Sweetwater (sweetwater.com, the US music instrument and pro audio retailer):
keyword search (42 results in Sweetwater's relevance order; a keyword that
opens a category takes sort and page) with the price, retail price, price
drops, rebates, special offers, units on hand, available and on order, and
open-box units; category listings (42 a page, facets); one item in full with
specs; the serial-numbered units of an instrument with each unit's weight and
photos; reviews (4 sorts, star filter, up to 100 a page); and the Deal Zone
pages. US only, prices in USD. Gear Exchange (used listings by private
sellers) is not covered. Namespace `sweetwater`, 6 endpoints: `search`,
`category`, `product`, `serial_units`, `reviews`, `deals`. Credits: 1 credit
each. `credits_used` in the response is what was charged. The request timeout
is raised to at least 240s.
See the [Sweetwater API
page](https://scavio.dev/sweetwater-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/sweetwater-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
sw = client.sweetwater
res = sw.search("boss delay pedal")["data"]
print(res["landed_on"], res["count"], res["currency"])
for it in res["items"][:5]:
    print(it["name"], it["price"], it["retail_price"], it["on_hand"], it["available"])
units = sw.serial_units("StratAU2HEUB")["data"]
print(units["name"], units["price"], units["count"])
for u in units["units"]:
    print(u["serial_number"], u["weight_lbs"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 135. Home goods -- Bed Bath & Beyond prices, online stock, delivery dates and stores

Bed Bath & Beyond (bedbathandbeyond.com, the US online home goods store):
keyword search and category listings (the site's sorts and facets, up to 84
pages) with the price, compare price (MSRP or was), discount, sale end and
promo badge, sponsored tiles kept apart; the department menu; one product with
every option's price, sale dates and exact online stock; a delivery estimate
for an option to a ZIP; reviews (4 sorts, star and text filters) and
questions; the deals page and its deal lists; and the stores of Bed Bath &
Beyond, The Container Store and Kirkland's near a ZIP, a point or in a state.
US only, prices in USD; online stock only (no store stock or store prices).
Namespace `bedbathbeyond`, 9 endpoints: `search`, `category`, `categories`,
`product`, `delivery_estimate`, `reviews`, `questions`, `stores`, `deals`.
Credits: 1 credit each; `search`, `category` and the deal lists of `deals` 2;
`product` occasionally 2. `credits_used` in the response is what was charged.
The request timeout is raised to at least 240s.
See the [Bed Bath & Beyond API
page](https://scavio.dev/bedbathbeyond-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/bedbathbeyond-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
bbb = client.bedbathbeyond
item = bbb.product("5296998")["data"]
print(item["name"], item["price"], item["compare_price"], item["compare_label"], item["on_sale"])
for opt in item["options"][:5]:
    print(opt["option_id"], opt["description"], opt["price"], opt["qty_on_hand"], opt["sale_end"])
eta = bbb.delivery_estimate("94445783", "10001")["data"]
for o in eta["options"]:
    print(o["name"], o["charge_text"], o["estimated_date"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 136. Brazil electronics -- KaBuM! card and Pix prices, offers with units left, sellers and shipping by CEP

KaBuM! (kabum.com.br, the Brazilian computer and electronics retailer):
keyword search and category listings (up to 100 a page, 5 sorts, facets) with
the card price, the Pix price (Pix is Brazil's instant payment) and the
running offer with its units left; the department and category tree; one
product with its spec sheet and, for a marketplace item, the seller's business
name, CNPJ and score; shipping options and dates to a CEP (a Brazilian postal
code); reviews with KaBuM!'s own summary (no reviewer names); and the Black
Friday and standing offers campaigns. Prices in BRL as shown to a visitor who
is not signed in, never a Prime price. Namespace `kabum`, 7 endpoints:
`search`, `category`, `categories`, `product`, `shipping`, `reviews`,
`offers`. Credits: 1 credit each. `credits_used` in the response is what was
charged. The request timeout is raised to at least 240s.
See the [KaBuM! API
page](https://scavio.dev/kabum-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/kabum-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
kabum = client.kabum
res = kabum.search("cadeira gamer")["data"]
print(res["total"], res["total_pages"], res["currency"])
for it in res["items"][:5]:
    print(it["name"], it["price"], it["cash_price"], it["list_price"], it["stock"])
deals = kabum.offers(campaign="blackfriday")["data"]
print(deals["campaign"]["name"], deals["campaign"]["ends_at"])
for it in deals["items"][:5]:
    print(it["name"], it["cash_price"], it["offer_units_left"], it["ends_at"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 137. Brazil retail -- Magazine Luiza prices, Pix prices, coupons, deal timers and stores

Magazine Luiza (magazineluiza.com.br, Magalu, the Brazilian retailer and
marketplace): keyword search, category and deal listings (40 a page, 8 sorts,
brand, seller, price, rating and attribute filters) with the price, the Pix
price (Pix is Brazil's instant payment), the coupon, the deal end time and the
seller; one product with installments, coupons, the seller's business data,
variants, specs and questions; reviews (no reviewer names); search
suggestions; Magalu stores by state and city; and one store with its address
and phone. Prices in BRL; shipping by CEP and store stock are not published.
Namespace `magalu`, 8 endpoints: `search`, `category`, `deals`, `product`,
`reviews`, `suggestions`, `stores`, `store`. Credits: 2 credits each.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s.
See the [Magazine Luiza API
page](https://scavio.dev/magalu-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/magalu-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
magalu = client.magalu
res = magalu.search("geladeira frost free")["data"]
print(res["total"], res["total_pages"], res["currency"])
for it in res["items"][:5]:
    print(it["title"], it["price"], it["pix_price"], it["coupon"], it["deal_ends_at"], it["seller"]["name"])
item = magalu.product("238058800")["data"]
print(item["title"], item["price"], item["pix_price"], item["pix_discount_percent"])
print(item["best_installment"]["description"], item["seller"]["name"], item["coupons"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 138. Brazil retail -- Casas Bahia, Extra and Ponto products, every seller's price and Pix price

Casas Bahia (casasbahia.com.br) and its Extra (extra.com.br) and Ponto
(pontofrio.com.br) storefronts, chosen with site: keyword search and category
listings (20 a page, 5 sorts, facet filters, own-store filter) with brand,
rating and status; list items carry no prices, so read product with an item's
sku; one product with the price, the Pix price (Pix is Brazil's instant
payment), installment plans and every seller's offer, specs, dimensions and
the page's reviews and questions; and the category menu. Prices in BRL.
Namespace `casasbahia`, 4 endpoints: `search`, `category`, `product`,
`categories`. Credits: 2 credits each. `credits_used` in the response is what
was charged. The request timeout is raised to at least 240s.
See the [Casas Bahia API
page](https://scavio.dev/casasbahia-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/casasbahia-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
cb = client.casasbahia
res = cb.search("geladeira frost free", site="casasbahia")["data"]
print(res["total"], res["total_pages"])
for it in res["items"][:5]:
    print(it["sku"], it["title"], it["brand"], it["status"])  # list items carry no prices
item = cb.product("55066339")["data"]
print(item["name"], item["price"], item["pix_price"], item["offer_count"])
for s in item["sellers"]:
    print(s)
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 139. Brazil price comparison -- Buscape and Zoom store offers, price history and coupons

Buscape and Zoom (buscape.com.br, zoom.com.br, Brazil's price comparison
sites; one catalog, chosen with site): keyword search, category and deal
listings with each product's lowest price and stores; one product with its
specs, the editors' pros and cons and store reviews (no reviewer names); every
store's offer for a product with cash and installment prices; up to 12 months
of the daily lowest price; the current lowest price; the campaign landing
pages; a store's coupons; search suggestions; and shipping estimates to a CEP
(a Brazilian postal code). Prices in BRL; store and coupon links are not
returned. Namespace `buscape`, 12 endpoints: `search`, `category`,
`categories`, `product`, `offers`, `price_history`, `lowest_price`, `deals`,
`deal_landing`, `store`, `suggestions`, `shipping`. Credits: 1 credit each.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s.
See the [Buscape API
page](https://scavio.dev/buscape-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/buscape-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
bp = client.buscape
offers = bp.offers("13994006", sort="price_asc")["data"]
print(offers["total"], offers["store_count"], offers["best_offer"]["price"])
for o in offers["offers"][:5]:
    print(o["store"]["name"], o["price"], o["installment_total"], o["stock"])
hist = bp.price_history("12755140")["data"]
print(hist["lowest"]["price"], hist["lowest"]["date"], hist["latest"]["price"])
for p in hist["points"][-7:]:
    print(p["date"], p["price"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 140. Brazil pharmacy retail -- Drogasil and Droga Raia prices, deals and store pickup

Drogasil and Droga Raia (drogasil.com.br, drogaraia.com.br, the pharmacy
chains of RD Saude, chosen with site): keyword, product code or EAN search,
category and deal listings (Oferta do Dia, % Especial, coupons, Black Friday)
with the price, list price and discount; the category tree; one product with
its variants and kits; prices for up to 48 product codes in one call; store
pickup yes or no for up to 5 product x store checks; stores near a CEP (a
Brazilian postal code) or by state, city and services; reviews with the site's
own summary (no reviewer names); and search suggestions. Regulatory flags are
returned exactly as the site gives them. Prices in BRL, the site's default
online price. Namespace `rdsaude`, 11 endpoints: `search`, `category`,
`categories`, `product`, `prices`, `store_availability`, `stores`,
`stores_search`, `reviews`, `deals`, `suggestions`. Credits: 1 credit each.
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s.
See the [Drogasil and Droga Raia API
page](https://scavio.dev/rdsaude-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/rdsaude-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
rd = client.rdsaude
res = rd.search("protetor solar")["data"]
print(res["site_name"], res["total"], res["currency"])
for it in res["items"][:5]:
    print(it["name"], it["brand"], it["price"], it["list_price"], it["in_stock"])
pickup = rd.store_availability(["38155"], ["200", "210"], site="drogaraia")["data"]
for sku in pickup["skus"]:
    print(sku["name"], [(s["store_id"], s["pickup_available"]) for s in sku["stores"]])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 141. Company reputation -- Reclame Aqui scores, complaints and rankings (Brazil)

Reclame Aqui (reclameaqui.com.br, Brazil's consumer complaint and company
reputation site): company search; one company's reputation by period
(complaints, answered and solved percent, would-do-business-again percent,
score and status), its main problems and segment position; the company's
complaints filtered by status, category, product, problem or words; one
complaint with its replies; complaint search across every company; the site's
11 ranking lists; and the segments with their best and worst companies. Text
in Portuguese as published; consumer names, emails and phones are never
returned. Namespace `reclameaqui`, 8 endpoints: `company_search`, `company`,
`complaints`, `complaint`, `complaint_search`, `rankings`, `segments`,
`segment_ranking`. Credits: 1 credit each; `complaints` 2 by `shortname` (the
company id is looked up first; 3 when the company page is read too).
`credits_used` in the response is what was charged. The request timeout is
raised to at least 240s.
See the [Reclame Aqui API
page](https://scavio.dev/reclameaqui-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/reclameaqui-company-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
ra = client.reclameaqui
co = ra.company("nubank")["data"]
print(co["name"], co["id"], co["verified"])
for r in co["reputation"]:
    print(r["period"], r["status_label"], r["final_score"], r["solved_percent"], r["complaints"])
res = ra.complaints(company_id=co["id"], status="resolved")["data"]
print(res["total"], res["total_pages"])
for c in res["complaints"][:5]:
    print(c["id"], c["title"], c["status"], c["solved"], c["score"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 142. Home improvement -- Leroy Merlin prices in 7 markets and exact store units in Brazil

Leroy Merlin (the home improvement retailer) in Brazil, Italy, Spain,
Portugal, Poland, Romania and France (country br, it, es, pt, pl, ro or fr):
keyword search (not France) and category listings with the price, original
price and promotion; one product with its specs, deliveries and marketplace
offers; exact store units with the aisle (Brazil only); stores and one store
with its hours; reviews (no reviewer names); and, for Brazil, shipping quotes
to a CEP (a Brazilian postal code), CEP lookup, the 28 price regions and the
department tree; search suggestions (it, es, pt, pl) and the Italian offers
listing. Brazil prices are set per region (region required). European listings
carry full details for the products the page shows in full and the rest as
ids. Prices in BRL, EUR, PLN or RON. Namespace `leroymerlin`, 13 endpoints:
`search`, `category`, `product`, `store_stock`, `stores`, `store`, `reviews`,
`shipping`, `cep`, `regions`, `categories`, `suggestions`, `offers`. Credits:
billed on what the request spent in its market: 1 credit in Brazil, Italy and
Romania (Italian product and category pages 2), 2 in Spain, Portugal and
Poland, 5 in France. `credits_used` in the response is what was charged. The
request timeout is raised to at least 240s.
See the [Leroy Merlin API
page](https://scavio.dev/leroymerlin-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/leroymerlin-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
lm = client.leroymerlin
res = lm.search("br", "furadeira", region="grande_sao_paulo")["data"]
print(res["total"], res["total_pages"], res["currency"])
for p in res["products"][:5]:
    print(p["id"], p["name"], p["price"], p["original_price"], p["unit"], p["in_stock"])
stock = lm.store_stock("br", id="85277934", region="rio_de_janeiro")["data"]
print(stock["unit"], stock["total_units"], stock["in_stock_count"])
for st in stock["stores"]:
    print(st["name"], st["units"], st["aisle"], st["pickup_in_store"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 143. Latin American beauty retail -- Natura prices, shades and Black Friday deals in 6 markets

Natura (the Brazilian beauty brand of Natura &Co) on its own storefronts in
Brazil, Argentina, Chile, Colombia, Mexico and Peru (country br, ar, cl, co,
mx or pe): keyword search, category and Black Friday campaign listings (up to
100 a page, the market's own sorts, the site's refinements and a price range)
with the sale price, the struck-through price and the discount; the category
menu; one product with every shade's price and stock flag, installments, kit
contents, ingredients and the rating with the 3 latest reviews (no reviewer
names); search suggestions; and the Natura stores in Brazil by state, city,
CEP prefix (a CEP is a Brazilian postal code) and store type. Prices in each
market's currency as shown to a visitor who is not signed in (no consultant or
regional prices). Namespace `natura`, 7 endpoints: `search`, `category`,
`categories`, `product`, `suggestions`, `stores`, `deals`. Credits: 1 credit
each. `credits_used` in the response is what was charged. The request timeout
is raised to at least 240s. See the [Natura API
page](https://scavio.dev/natura-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/natura-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
natura = client.natura
res = natura.search("perfume")["data"]
print(res["total"], res["total_pages"], res["currency"])
for it in res["items"][:5]:
    print(it["product_id"], it["name"], it["price"], it["list_price"], it["discount_percent"])
item = natura.product("NATBRA-194225")["data"]
print(item["name"], item["price"], item["list_price"], item["in_stock"], item["low_stock"])
for s in item["shades"]:
    print(s["shade"], s["price"], s["in_stock"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 144. Brazil beauty retail -- O Boticario and Eudora card and Pix prices, shades, reviews and store pickup

O Boticario and Eudora (boticario.com.br, eudora.com.br, the beauty brands of
Grupo Boticario, chosen with brand): keyword search, category and deal
listings (Beauty Week, the site's Black Friday event, and the promotions hub;
36 a page, 7 sorts, product brand, line, category, rating, price and facet
filters) with the card price, the Pix price (Pix is Brazil's instant payment),
the was price, deal badges and each item's countdown end; the category menu;
each campaign's dates and coupon codes from the promotions conditions page;
one product by slug, link or SKU with its online stock count, every shade and
size, kit contents and the review summary; current prices for up to 10 SKUs;
reviews by SKU or for every shade together (no reviewer names); pickup stores
near a CEP (a Brazilian postal code); a product's delivery options at a CEP
and whether store pickup is offered there; and search suggestions. Prices in
BRL. Namespace `boticario`, 11 endpoints: `search`, `category`, `categories`,
`deals`, `promotions`, `product`, `prices`, `reviews`, `stores`, `pickup`,
`suggestions`. Credits: 1 credit each; `search`, `category`, `categories`,
`deals`, `promotions` and `product` 2 when the page needs a second route;
`prices` 1 per 5 SKUs. `credits_used` in the response is what was charged. The
request timeout is raised to at least 240s. See the [O Boticario and Eudora
API
page](https://scavio.dev/boticario-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/boticario-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
bot = client.boticario
res = bot.search("perfume")["data"]
print(res["total"], res["total_pages"], res["currency"])
for it in res["items"][:5]:
    print(it["sku"], it["name"], it["price"], it["pix_price"], it["was_price"], it["badges"])
prices = bot.prices(["B01863", "B48734", "B2022081233"])["data"]
for it in prices["items"]:
    print(it["sku"], it["found"], it["price"], it["was_price"], it["pix_price"])
quote = bot.pickup("01310-100", sku="B2022081233")["data"]
print(quote["click_and_collect"], [(d["description"], d["shipping_cost"]) for d in quote["delivery"]])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

### 145. Brazil sporting goods -- Centauro prices, sizes, freight and store pickup by CEP

Centauro (centauro.com.br, the sporting-goods retailer of Grupo SBF): keyword
search, category and deal listings (Black Friday, outlet, Mega Oferta; 36 a
page, 4 sorts, filtered by brand, size, gender, sport, store, sold-by and any
facet) with the price, list price, discount, the Pix price (Pix is Brazil's
instant payment) where the site shows one and the other colours; one product
(model + colour) with every size's sku, EAN, price, stock flag and seller;
delivery options and store pickup for one size to a CEP (a Brazilian postal
code), with each nearby store's stock flag and pickup time; stores near a CEP;
and search suggestions. Prices in BRL; stock flags, not unit counts. Namespace
`centauro`, 7 endpoints: `search`, `category`, `deals`, `product`, `freight`,
`stores`, `suggestions`. Credits: 1 credit each. `credits_used` in the
response is what was charged. The request timeout is raised to at least 240s.
See the [Centauro API
page](https://scavio.dev/centauro-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
and the
[docs](https://scavio.dev/docs/centauro-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient()
cen = client.centauro
res = cen.search("tenis corrida")["data"]
print(res["total"], res["total_pages"], res["currency"])
for it in res["items"][:5]:
    print(it["product_id"], it["name"], it["price"], it["list_price"], it["discount_percent"], it["pix_price"])
item = cen.product("9976EA51")["data"]
for s in item["sizes"][:5]:
    print(s["size"], s["sku"], s["price"], s["in_stock"], s["seller"]["name"])
fr = cen.freight("9976EA510375", "01310-100")["data"]
for o in fr["delivery_options"]:
    print(o["type"], o["label"], o["cost"], o["estimated_text"])
for st in fr["stores"][:5]:
    print(st["name"], st["in_store_stock"], st["pickup_text"])
```

Failed calls and refused inputs are not charged; a not-found is charged.
Inputs the API only accepts to refuse are not in the method signatures.

## Error Handling

```python
from scavio import (
    ScavioClient,
    InvalidAPIKeyError,
    RateLimitError,
    InsufficientCreditsError,
    NotFoundError,
    BadRequestError,
    ScavioConnectionError,
    ScavioTimeoutError,
    ScavioAPIError,
    ScavioError,
)

client = ScavioClient(api_key="sk_...")

try:
    results = client.search("query")
except InvalidAPIKeyError:
    print("Check your API key")
except RateLimitError:
    print("Too many requests - upgrade your plan")
except InsufficientCreditsError:
    print("Out of credits - purchase more at dashboard.scavio.dev")
except ScavioAPIError as e:
    # Any other non-2xx response; inspect the details:
    print(e.status_code, e.response_body)
```

All exceptions inherit from `ScavioError`. HTTP errors (`BadRequestError` 400,
`InvalidAPIKeyError` 401, `InsufficientCreditsError` 402, `NotFoundError` 404,
`RateLimitError` 429, `ScavioAPIError` for anything else) carry `.status_code`
and `.response_body`. Network failures raise `ScavioConnectionError` /
`ScavioTimeoutError` after retries are exhausted.

## Configuration

```python
client = ScavioClient(
    api_key="sk_...",
    base_url="https://api.scavio.dev",  # custom base URL
    timeout=30.0,                        # request timeout in seconds
    max_requests_per_second=1,           # client-side rate limit (1-50)
    max_retries=2,                       # retries on 429/5xx/network (0 disables)
)
```

### Async client

The async client mirrors the sync one method-for-method. It keeps a single
pooled `httpx.AsyncClient` alive for its lifetime; close it with
`await client.aclose()` or use the async context manager.

```python
import asyncio
from scavio import AsyncScavioClient

async def main():
    async with AsyncScavioClient(api_key="sk_...") as client:
        return await client.google.search("openai", gl="us")

asyncio.run(main())
```

## Integrations

Scavio works with popular AI/LLM frameworks:

- [LangChain](https://github.com/scavio-ai/langchain-scavio) -- `pip install langchain-scavio`
- [MCP Server](https://www.npmjs.com/package/@scavio/mcp-server) -- for Claude, Cursor, and other MCP clients
- [n8n](https://www.npmjs.com/package/n8n-nodes-scavio) -- no-code workflow automation

## API Reference

| Service | Endpoints | Credits |
|---------|-----------|---------|
| Google | `search`, `custom_search`, `ai_mode`, `maps_search`, `maps_place`, `maps_reviews`, `shopping`, `shopping_product`, `shopping_stores`, `flights`, `hotels`, `hotels_detail`, `news`, `trends`, `trending` | 1 each |
| Amazon | `search`, `product`, `offers`, `options` | 1 each (`options` free) |
| Walmart | `search`, `product`, `stores`, `reviews`, `category`, `offers`, `seller`, `seller_products` | 1, except `search`/`category` on `domain="com.mx"` and store-targeted `search`/`product` (`delivery_zip` + `store_id`), which cost 2 |
| YouTube | `search`, `shorts`, `suggestions`, `video`, `metadata` (deprecated alias of `video`), `comments`, `comment_replies`, `transcript`, `related`, `channel_search`, `channel`, `channel_videos`, `channel_shorts`, `channel_community`, `channel_resolve`, `streams`, `community_post`, `community_post_comments` | `search`/`shorts` 2, `transcript` 5, `streams` 3, rest 1 each |
| Reddit | `search`, `search_suggestions`, `post`, `post_comments`, `comment_replies`, `subreddit`, `subreddit_posts`, `user`, `user_posts`, `user_comments`, `popular`, `trending`, `search_comments`, `search_subreddits` | 1 each |
| X | `search`, `tweet`, `tweet_comments`, `tweet_retweeters`, `user`, `user_tweets`, `user_replies`, `user_media`, `user_followers`, `user_followings`, `trending`, `search_communities`, `community`, `community_tweets` | 1 each |
| TikTok | `profile`, `user_posts`, `video`, `video_transcript`, `video_comments`, `comment_replies`, `search_videos`, `search_users`, `hashtag`, `hashtag_videos`, `user_followers`, `user_followings`, `trending_searches`, `trending_videos`, `search_suggestions`, `music`, `music_videos`, `search_music`, `music_chart`, `user_similar`, `user_playlists`, `playlist_videos`, `user_live`, `user_region` | 1 each |
| TikTok Shop | `search`, `search_suggestions`, `product`, `product_reviews`, `categories`, `category_products`, `shop_products`, `resolve` | 1 each |
| Instagram | `profile`, `user_posts`, `user_reels`, `user_tagged`, `user_stories`, `post`, `post_comments`, `comment_replies`, `search_users`, `search_hashtags`, `user_followers`, `user_followings`, `user_highlights`, `highlight_stories`, `search_reels`, `search_music`, `music_posts`, `search_locations`, `user_similar`, `post_likers` | Typically `profile`/`user_reels`/`user_tagged`/`music_posts` 1 (`user_reels`/`user_tagged` 2 the first time a username is looked up), every other method 2; `search_users`/`search_hashtags` with a `cursor` 8. Any call can cost up to 10 when it needs extra work; `credits_used` is the exact charge |
| LinkedIn | `person`, `person_about`, `person_posts`, `person_contact`, `company`, `company_posts`, `company_people`, `company_jobs`, `search_people`, `search_jobs`, `search_posts`, `job`, `post`, `post_comments` | `job` 30, `person_posts`/`company_posts`/`search_jobs`/`post_comments` 10 each, `person`/`person_about`/`company`/`post` 1 each; the five retired endpoints (`person_contact`, `company_people`, `company_jobs`, `search_people`, `search_posts`) return 410 and are never billed |
| Threads | `profile`, `user_posts`, `user_replies`, `post`, `post_comments`, `search_users` | 2, but `profile`/`user_posts`/`user_replies` cost 4 when addressed by `username` instead of `user_id` |
| Kuaishou | `profile`, `user_posts`, `user_live`, `user_resolve`, `video`, `video_comments`, `comment_replies`, `videos_batch`, `search`, `search_videos`, `search_users`, `search_live`, `tag_feed`, `trending` | priced per endpoint: `videos_batch` 40, `profile` and the four `search*` 10 each, `video` 2, the rest 1 |
| eBay | `search` (live or sold listings), `product`, `seller` | 1 each |
| Target | `search`, `category`, `product`, `reviews`, `availability` | 1 each |
| Home Depot | `search`, `product`, `reviews`, `stores`, `availability` (`country="ca"` for Home Depot Canada), `shipping` (US only); Canada only: `category`, `categories`, `stock`, `store`, `suggestions` | 2 each in the US, `shipping` 4; 1 each for Canada |
| Zillow | `search`, `property`, `agent_reviews` | 1 each |
| Redfin | `search`, `property`, `market` | 1 each |
| Realtor.com | `search`, `property`, `locations`, `market`, `agents`, `agent` | 1 each |
| Rightmove | `locations` (start here), `search`, `property`, `sold`, `sold_property`, `agents`, `agent` | 1 each |
| Rent.com (`rentcom`) | `search`, `listing`, `building`, `rent_trends`, `suggestions`, `cities`; US; `site` rent (default) or apartmentguide; `search` takes `city` and `state` or `zip` | 1 each |
| Trulia (`trulia`) | `neighborhood`, `search`, `property`, `school`, `suggestions`; US; `language` en or es (rental search, buildings, neighborhoods); `property` takes `zpid`, `building_id` or `url` | 1 each |
| StreetEasy (`streeteasy`) | `search`, `listing`, `building`, `buildings`, `market`; NYC and North NJ; `mode` sale, rent or sold; `listing` by `url`, or `id` with `listing_type`; `market` NYC only | 1 each |
| RentCafe (`rentcafe`) | `search`, `property`, `floorplan_units`, `reviews`, `suggestions`, `rent_trends`; `market` us or ca, `language` en or fr; one of beds, rent specials, short-term, furnished, utilities included or an amenity per search | 1 each |
| Movoto (`movoto`) | `search`, `property`, `market_trends`, `suggestions`, `school`; US; `search` by `city` and `state`, `zip`, `county`, `neighborhood` or `school_id`; `status` for_sale, sold or rentals; `property` and `school` by `url` or `path` | 1 each |
| HotPads (`hotpads`) | `search`, `listing`, `price_history`, `fees`, `suggestions`; US; `search` takes an `area` (a `suggestions` id or a place such as Austin, TX); `price_history` and `fees` take the listing's `listing_alias` | 1 each |
| Apartment List (`apartmentlist`) | `suggestions`, `search`, `listing`, `rent_report`, `market_summary`, `review_summaries`; US; `search` and `market_summary` take `location`, `city` and `state` or `zip`; `rent_report` and `review_summaries` a city | 1 each |
| Compass (`compass`) | `search`, `listing`, `suggestions`; US; `search` takes an `area` slug and `mode` for_sale, for_rent or sold; `listing` by `url` or `id` | 2 each |
| AffordableHousing.com (`affordablehousing`) | `search`, `listing`, `suggestions`, `waiting_lists`, `housing_authority`, `housing_authorities`; US; `search` and `housing_authorities` take a `state`; `housing_authority` by `url`, or `id` with `state` | `search` and `suggestions` 2; the rest 1 |
| Lennar (`lennar`) | `search`, `community`, `plan`, `home`, `master_planned`, `markets`, `market`, `suggestions`, `resolve`, `promotions`, `payment`; US; `search` by `market`, `state`, `city`, `text`, a point or `bounds`; `payment` takes a homesite and its community, a down payment and an interest rate | 1 each |
| Extra Space Storage (`extraspace`) | `search`, `facility`, `reviews`, `city_prices`, `locations`; US; `search` by `term` (ZIP, city or place) or a point; `facility` and `reviews` by `store_id` or `url` | 1 each |
| Public Storage (`publicstorage`) | `search`, `facility`, `reviews`; `market` us or ca, `language` en or fr; `search` by `location` or `slug`; `reviews` US facilities | 1 each |
| U-Haul (`uhaul`) | `truck_quote`, `locations`, `location`, `storage_search`, `storage_facility`, `reviews`, `suggestions`, `supplies`; US and Canada, `language` en, es or fr; `truck_quote` takes `pickup`, `date` and an optional `dropoff` (never a reservation); `location`, `storage_facility` and `reviews` by id or `url`; `supplies` by `category` or `url`, `country` us or ca | 1 each |
| Booking.com | `search`, `hotel`, `reviews` | 1 each |
| Tripadvisor | `locations` (start here), `search`, `location`, `reviews` | 2 each |
| Airbnb | `search`, `listing`, `reviews` | 1 each |
| Vrbo (`vrbo`) | `search`, `property`, `suggestions`; 20 market-languages (`market`); `search` needs dates, the first 50 results; `property` without dates | `search` 2 per attempt (2 to 8); the rest 2 |
| Expedia (`expedia`) | `search`, `property`, `price_calendar`, `suggestions`; 51 market-languages (`market`); `search` needs dates, the top results of the first page; `property` without dates; hotel pages held in en-gb, pt-br, zh-hk, en-hk, zh-hans-hk, en-my, en-ph | 2 each, billed on actual cost (1 on some pages) |
| Yelp | `search`, `business`, `reviews` | 2 each |
| Indeed | `search`, `job`, `company`, `company_reviews` | 2 each |
| Glassdoor | `companies` (start here), `company`, `reviews`, `salaries` | 1 each |
| Apple App Store | `search`, `app`, `reviews` | 1 each |
| Google Play | `search`, `app`, `reviews` | 2 each |
| SEC EDGAR | `lookup` (start here), `company`, `filings`, `concept`, `facts`, `search` | 1 each |
| Companies House | `search` (start here), `company`, `officers`, `filing_history` | 1 each |
| G2 | `search`, `product`, `reviews` | 5 each |
| Capterra | `search`, `product`, `reviews` | 2 each |
| Google Ads Transparency | `advertisers` (start here), `search`, `creative` | 1 each |
| Meta Ad Library | `search`, `advertiser`, `ad` | 1 each |
| Costco | `search`, `category`, `categories`, `product`, `prices`, `availability`, `reviews`, `warehouses`, `gas`, `coupons`, `deals`, `clearance`, `autocomplete` | 1 each, except `prices` (2 at 10 warehouses), `availability` (1 per 5 warehouses), `warehouses` (2 with `country="ca"`) and `gas` (2 by location on ca; by `warehouse_ids`, 1 per 5 on us and 2 per warehouse on ca) |
| BJ's Wholesale Club (`bjs`) | `product`, `search`, `category`, `categories`, `reviews`, `coupons`, `clubs`; US; `search` and `category` list 40 results, priced for the club BJ's assigns; `product` and `reviews` by `product_id` or `url`; `clubs` by `state` | 1 each |
| Lowe's | `stores` (start here), `search`, `product`, `reviews` | `reviews` 1, the rest 2 each |
| Sam's Club | `clubs`, `search`, `product`, `savings`, `category`, `reviews` | `clubs` 1, the rest 2 each |
| Canadian Tire | `stores` (start here), `search`, `product`, `availability`, `clearance`, `deals` | 1 each |
| SportChek (`sportchek`) | `search`, `list`, `product`, `reviews`, `suggestions`, `store`, `brands`, `categories`; Canada, English only; `product` and `reviews` take `code` or `url`, `list` takes `path` or `url` | 1 each |
| Mark's (`marks`) | `search`, `list`, `product`, `questions`, `suggestions`, `store`, `brands`, `categories`; Canada; `language` en or fr (L'Equipeur) on `search`, `list`, `product`, `brands`, `categories` | 1 each |
| RONA (`rona`) | `search`, `product`, `prices`, `category`, `categories`, `stores`, `store`, `stock`, `deals`; Canada; `language` en or fr on every method; `prices` takes up to 60 `skus` and a `store_id` (required) | `prices`, `categories`, `stores`, `store` 1; `search` and `deals` 2 (3 with `store_id`); `product` and `stock` 3; `category` 1-3 |
| PC Express (`pcexpress`) | `search`, `category`, `collection`, `product`, `stores`, `store`, `suggestions`; Canada; `banner` (10, default superstore) and `language` en or fr (fr on provigo and maxi); prices are each banner's default store's | `product` and `store` 5 (`product` 1 when it answers from the search listing); the rest 1 each |
| Dollar General | `stores` (start here), `search`, `product`, `deals`, `coupons` | 1 each |
| Sephora | `search`, `category`, `product` (`country="ca"` for Sephora Canada); Canada only: `brand`, `brands`, `suggestions`, `offers`, `stores`, `store` | 1 each; `product` and `offers` 2 (the same in both countries) |
| Ulta Beauty | `search`, `category`, `product`, `stores` | 1 each |
| ALDI | `stores` (start here), `search`, `product` | 1 each |
| Micro Center | `stores` (start here), `search`, `product` | `stores` 1, the rest 2 each |
| Walgreens | `stores` (start here), `search`, `product`, `stock` | `stock` 4, the rest 2 each |
| CVS | `search`, `product`, `stock` | 1 each |
| Whole Foods Market | `stores` (start here), `store`, `search`, `category`, `deals`, `product`, `sales_flyer` | 1 each |
| Harbor Freight | `search`, `clearance`, `product`, `prices`, `stores`, `availability`, `reviews` | 1 each |
| PetSmart | `search`, `product`, `stores`, `store_stock`, `availability`, `deals` | 1 each |
| Petco | `search`, `category`, `product`, `stores`, `store_inventory` | 1 each |
| iHerb | `search`, `product`, `prices`, `reviews` | 2 each |
| Chewy | `search`, `product` | 10 each |
| Menards | `search`, `stores`, `product` | `search` 2; `stores` and `product` 1 each, `product` with `store_id` 2 |
| Nordstrom | `search`, `category`, `brand`, `product`, `reviews`, `availability`, `stores`, `suggestions` | `availability` and `reviews` 10, the rest 5 each |
| Nordstrom Rack (`nordstrom_rack`) | `search`, `category`, `brand`, `product`, `reviews`, `availability`, `stores`, `suggestions` | `availability` and `reviews` 10, the rest 5 each |
| Best Buy (`best_buy`) | `search`, `product`, `reviews`, `category`, `deals`, `stores`, `availability`, `suggestions`, `prices` (`country="ca"` for Best Buy Canada); Canada only: `questions` | US: `stores` and `suggestions` 1; `deals` 3; `category` 2, 3 on a `pcmcat` page; the rest 2 each (`prices` per call, up to 15 SKUs; `availability` flat, up to 8 stores). 1 each for Canada |
| Newegg (`newegg`) | `search`, `category`, `categories`, `product`, `offers`, `reviews`, `deals`, `seller`, `seller_products`, `suggestions`; `country` us, ca or a Newegg Global storefront (uk, au, nz, jp, ph, sg, kr, th, mx); `offers` us and ca; `reviews` takes the product's `group_id` and `subcategory_id` | 2 each |
| Sweetwater (`sweetwater`) | `search`, `category`, `product`, `serial_units`, `reviews`, `deals`; US; free-text `search` shows 42 results (a keyword that opens a category takes `sort` and `page`); `product`, `serial_units` and `reviews` by `item_id` or `url` | 1 each |
| TCGplayer | `search`, `product`, `listings`, `price_history`, `sales`, `games`, `sets`, `price_guide`, `suggestions`, `trending`, `seller`, `seller_feedback`, `seller_products` | 1 each |
| Vinted | `search`, `product`, `seller`, `seller_products`, `seller_feedback`, `brands`, `suggestions`, `filters`, `categories` | 1 each |
| Macy's (`macys`) | `search`, `product`, `reviews`, `category`, `brand`, `deals`, `stores`, `store_availability`, `suggestions` | 1 each |
| Gap Inc. (`gap`) | `search`, `category`, `categories`, `product`, `prices`, `stores`, `store`, `store_stock`, `suggestions`, `trending`, `deals`; `brand` gap, old_navy, banana_republic, athleta, gap_factory or banana_republic_factory; `country` us or ca, `language` en or fr; `store_stock` takes 1 to 10 `store_ids` and `sku_ids` or a `style_id` | 1 each |
| Abercrombie & Fitch (`abercrombie`) | `search`, `product`, `store_stock`, `stores`, `store`, `category`, `categories`, `promotions`, `reviews`, `suggestions`; `brand` anf or hol; `storefront` us, us_es, ca, ca_fr, uk, eu, eu_de, eu_fr, eu_es, eu_it, eu_nl, am, am_zh, am_ja, wd or wd_es (`country` picks the ship-to country on eu and wd); `store_stock` takes 1-10 `skus` and a `zip` or a point | 1 each, `reviews` 2 without a `url` |
| Bath & Body Works (`bathandbodyworks`) | `search`, `category`, `categories`, `product`, `promotions`, `offers`, `store_availability`, `store`, `stores`, `reviews_summary`; `country` us or ca; `search` and `category` show 48 results (no page 2); `product`, `promotions`, `store_availability` and `reviews_summary` by `product_id` or `url` | 1 each |
| Williams-Sonoma (`williamssonoma`) | `product`, `configurator`, `delivery_estimate`, `stock`, `store_pickup`, `stores`, `floor_samples`, `categories`, `category`, `search`, `popular_searches`, `reviews`; `brand` williams_sonoma, pottery_barn, pottery_barn_kids, pottery_barn_teen, west_elm, rejuvenation or mark_and_graham; `market` us (ca on `product`); `product`, `stock` and `reviews` by `product` or `url`; `store_pickup` takes up to 20 `skus` and 10 `stores` | 1 each, `search` and `category` 5 |
| Bed Bath & Beyond (`bedbathbeyond`) | `search`, `category`, `categories`, `product`, `delivery_estimate`, `reviews`, `questions`, `stores`, `deals`; US; `search` by `query` or a `facet_url`; `category` by `slug` + `category_id` or `url`; `product`, `reviews` and `questions` by `product_id` or `url`; `delivery_estimate` takes an `option_id` and a `zip`; `deals` is the deals page or a deal list (`type`) | 1 each, `search`, `category` and deal lists 2 |
| QVC + HSN (`qvc`) | `search`, `product`, `products`, `todays_special`, `on_air`, `program_guide`, `recently_aired`, `category`, `suggestions`, `reviews`; `site` qvc or hsn; QVC `market` us, uk, de, it or jp (each endpoint lists the markets it serves), HSN us; `product` and `reviews` by `item_number` or `url`; `products` takes up to 20 `item_numbers`; `recently_aired` hsn only; `reviews` is the first page | 1 each |
| Saks Fifth Avenue (`saks`) | `search`, `product`, `category`, `brand`, `deals`, `stores`, `store_availability`, `suggestions`, `designers` | 2 each |
| Kohl's (`kohls`) | `search`, `product`, `category`, `brand`, `deals`, `stores`, `store_availability`, `suggestions`, `coupons` | `stores` 1, the rest 2 each |
| Belk (`belk`) | `search`, `category`, `deals`, `categories`, `product`, `variant`, `store_availability`, `stores`, `store`, `reviews`; US; `search`, `category` and `deals` 60 items a page, filtered by brand, color, size, sales promotion, coupon code, discount band, price and pickup store; `product` and `reviews` by `product_id` or `url`; `store_availability` takes 1-10 `store_ids` and a `variant_id` (with its `orin`, from `variant`) or up to 5 `items`; `reviews` is the 8 newest | 2 each; `product` and `variant` up to 4, `store_availability` 1 plus 2 per looked-up variant |
| Rakuten (`rakuten`) | `stores`, `store`, `store_coupons`, `rates`, `search`, `suggestions`, `category`, `deals`, `in_store`; `country` us, gb or ca (`language` en or fr on ca); `rates` checks up to 100 `store_ids`; `store` and `store_coupons` by store slug or id | 1 each |
| JCPenney (`jcpenney`) | `search`, `product`, `category`, `brand`, `deals`, `stores`, `store_availability`, `suggestions`, `coupons`, `reviews`, `questions` | 1 each |
| Dick's Sporting Goods (`dicks`) | `search`, `product`, `products`, `reviews`, `category`, `brand`, `deals`, `store_availability`, `suggestions` | `product` and `reviews` 2, the rest 1 each |
| Academy Sports + Outdoors (`academy`) | `search`, `product`, `store_availability`, `stores`, `store`, `category`, `categories`, `deals`, `suggestions`; US; `search` by `query`; `product` by `url` or `slug`; `store_availability` takes a `part_number`, a `store_id` and its `state`; `stores` by `zip` or a point | 1 each |
| REI (`rei`) | `search`, `category`, `deals`, `product`, `reviews`, `store_stock`, `stores`, `store`, `suggestions`; US; `category` by `slug` or `url`; `product` and `reviews` by `product_id` or `url`; `store_stock` takes a `sku` and a `zip`, a `city` and `state` or a point | 2 each |
| L.L.Bean (`llbean`) | `search`, `category`, `categories`, `product`, `store_stock`, `stores`, `reviews`, `review_summary`, `delivery_estimate`, `suggestions`, `deals`; `market` us, ca or intl (with a `country`) on `search`, `category`, `product` and `deals`; the rest US; `store_stock` takes an `item_id` and `store_ids` or `all_stores`; `stores` by `zip`, a point, `city` + `state`, `store_ids` or `all_stores` | 1 each |
| Foot Locker (`footlocker`) | `search`, `product`, `category`, `brand`, `deals`, `releases`, `stores`, `store_availability`, `reviews`, `questions` | 1 each |
| Zappos (`zappos`) | `search`, `product`, `reviews`, `questions`, `lowest_prices`, `categories`, `suggestions`; `site` zappos or 6pm; `product` by exactly one of `product_id`, `style_id`, `stock_id` or `asin`; `reviews`, `questions` and `lowest_prices` zappos only | 1 each |
| Fanatics (`fanatics`) | `search`, `product`, `browse`, `deals`, `reviews` | 1 each |
| Argos (`argos`) | `search`, `product`, `store_stock`, `stores`, `reviews`, `questions`, `categories`, `category`, `deals`, `suggestions`; one UK store (argos.co.uk, GBP), no `country` | 2 each |
| Media Expert (`mediaexpert`) | `search`, `product`, `store_stock`, `stores`, `reviews`, `category`, `categories`, `brands`, `brand`, `promotions`, `outlet`, `seller`, `suggestions`; one Polish store (mediaexpert.pl, PLN), no `country` | actual cost, 1 to 3: `store_stock` and `categories` 2; `search` 3 (1 when it redirects to a full category page); `category`, `brand`, `outlet`, `seller` and promotion-list products 1 unsorted, 3 sorted or lazily loaded; the rest 1 |
| Action (`action`) | `search`, `product`, `products`, `category`, `categories`, `brand`, `brands`, `new_arrivals`, `weekly_deals`, `collection`, `suggestions`, `stores`, `store`, `reviews`, `webshop_search`, `webshop_product`; 19 storefronts (`country`, plus `language` for be and ch); `reviews` nl, de, fr, pl; webshop nl, be | 1 each |
| HEMA (`hema`) | `search`, `product`, `category`, `categories`, `new_arrivals`, `sale`, `offers`, `campaign`, `suggestions`, `store_stock`, `stores`, `store`, `reviews`; webshops nl, be (`language` nl or fr), fr, de; `store_stock` and `stores` also lu and at; `sale` nl, be, de; `offers` nl, be | 1 each |
| AutoZone (`autozone`) | `search`, `product`, `category`, `brand`, `vehicles`, `reviews`, `stores`, `store`, `categories`, `clearance`, `rebates`, `store_stock`; us (default); br on `search`, `product`, `vehicles`, `stores`, `store`, `categories`, `store_stock` (Brazil only); mx on `vehicles`, `stores`, `store`, `categories` | 1 each; `search` and `product` with `country="br"` and `store_stock` 2 |
| O'Reilly Auto Parts (`oreilly`) | `search`, `cross_reference`, `product`, `vehicles`, `compatibility`, `category`, `categories`, `brand`, `store_stock`, `stores`, `store`, `suggestions`, `rebates`, `deals`; us (default) on every method; mx on `stores` and `store` only (the Mexican store directory, in Spanish) | 2 each; `product` by `line_code` + `part_number` 4; `cross_reference` 2 / 4 / 6 by inputs; `brand` index 4; `store_stock` and `stores` by `zip` 4; `deals` 4 |
| RockAuto (`rockauto`) | `vehicles`, `categories`, `parts`, `search`, `brand`, `brands`, `part`, `suggestions`, `resolve`, `tools`, `promotions`; start with `vehicles` (make, year, model, engine, `carcode`); `currency` (15) and `language` en, es, fr, de | 1 each |
| Cars.com (`carscom`) | `search`, `listing`, `dealer`, `dealer_inventory`, `dealer_reviews`, `model_reviews`, `dealers`, `research`; US; `search` and `dealers` take a `zip` | 1 each |
| Autotrader (`autotrader`) | `search`, `listing`, `dealers`, `dealer`, `makes`; US; `search` and `dealers` take a `zip` | 2 each |
| CarGurus (`cargurus`) | `search`, `dealer`, `dealers`, `price_trends`, `research`, `expert_reviews`, `makes`, `models`; `market` us (default), us-es, ca, ca-fr, uk; no listing detail | 1 each |
| CarMax (`carmax`) | `search`, `listing`, `photos`, `stores`, `store`, `store_inventory`, `reviews`, `review_summary`, `suggestions`, `makes`, `models`, `car_value`; US; `search` takes a `zip`; `stores` one of `zip`, `state`, `city` | 1 each |
| Carvana (`carvana`) | `search`, `vehicle`, `model_guide`, `trims`, `make`, `makes`; US; by make and model, `city` (Carvana's city pages), no ZIP | 1 each |
| TrueCar (`truecar`) | `search`, `listing`, `model`, `reviews`, `dealer`, `dealer_inventory`, `suggestions`, `makes`, `models`; US; `search` takes a `zip`; `listing` by VIN (input only) or link | 1 each |
| Edmunds (`edmunds`) | `search`, `listing`, `reviews`, `dealer`, `model`, `price`, `appraisal`, `makes`; US; `search` takes `city` and `state`; `listing` by VIN (input only) with make, model and year, or link | 2 each |
| Kelley Blue Book (`kbb`) | `car_value`, `model`, `search`, `listing`, `reviews`, `dealers`, `dealer`, `makes_models`; US; `car_value` by make, model, year and trim, optionally at a `zip` (not for buy_new) | 1 each; `car_value` at a `zip` 2 (up to 6); deeper `reviews` up to 5 |
| Ace Hardware (`acehardware`) | `search`, `product`, `store_stock`, `store`, `stores`, `category`, `categories`, `brand`, `deals`, `weekly_ad`, `paint_colors`; us only (no `country`); store methods take a 5-digit Ace store number | 1 each; `search` 2 (3 on a category redirect); `product` 2; `store_stock` 1 per 5 stores (`nearby` 6); `stores` with `details` 1 lookup per store (25 stores 6) |
| Tractor Supply (`tractorsupply`) | `search`, `product`, `store_prices`, `store_stock`, `fulfillment`, `stores`, `store`, `category`, `categories`, `brand`, `deals`, `promotions`; us only (no `country`); `search`, `product`, `category`, `brand` and `deals` need `store` or `zip` | 1 each; `product` 2 on the first call for a store not yet looked up; `store_prices` 1 per 5 lookups (25 new stores 11) |
| Michaels (`michaels`) | `search`, `product`, `store_stock`, `store_inventory`, `stores`, `store`, `category`, `categories`, `brand`, `deals`, `suggestions`; us (default) on every method; ca (English or French) on every method except `stores`, `categories` and `suggestions` | 2 each; `category` and `deals` 4 with a `/shop/` category |
| Nike (`nike`) | `search`, `product`, `category`, `brand`, `deals`, `releases`, `release`, `reviews`; 62 storefronts in 42 countries (`country` + `language`); `releases` and `release` not on vn, cn or jp in English; `reviews` not on cn | 1 each |
| Staples (`staples`) | `search`, `product`, `category`, `categories`, `deals`, `coupons`, `store_stock`, `stores`, `store`, `reviews`, `questions`, `trending`; us (default) on every method; ca (English or French) on `search` and `product` only | 1 each |
| Dollar Tree (`dollartree`) | `search`, `product`, `category`, `categories`, `brand`, `deals`, `store_stock`, `stores`, `store`, `reviews`; us only (no `country`) on every method except `store`, which also takes ca (Canada store pages); `store_stock` needs a store number | 1 each; `stores` 5 |
| Discount Tire (`discounttire`) | `search`, `vehicle`, `vehicle_tires`, `product`, `model`, `store_stock`, `stores`, `store`, `reviews`, `store_reviews`, `wheels`, `browse`, `categories`, `suggestions`, `appointments`; us only (no `country`); `search`, `vehicle_tires`, `product`, `model`, `wheels` and `browse` need `store` or `zip` | 1 each |
| Vevor (`vevor`) | `search`, `product`, `shipping`, `reviews`, `questions`, `suggestions`, `categories`, `category`, `collections`, `deals`, `prices`; 13 storefronts (`country` + `language`) on every method except `prices`, which takes `sku` only and asks every storefront; `shipping` needs `state` (us) or `province` (ca) | 1 each; `prices` 3 |
| Nellis Auction (`nellis`) | `search`, `item`, `locations`, `categories`; `location` (6 shopping locations, default `las-vegas`) on `search`, `locations` and `categories`; `item` takes `id` or `url`; search lists open auctions only | 1 each |
| Bring a Trailer (`bringatrailer`) | `results`, `price_history`, `listing`, `live`, `make`, `model`, `location`, `suggestions`; one site; amounts in each lot's own currency | 1 each |
| Dermstore (`dermstore`) | `search`, `list`, `product`, `suggestions`, `offers`, `brands`, `categories`; `country` (`us` default, or `ca` in Dermstore's own CAD prices) on every method; `list` takes `path` or `url`, `product` takes `sku` or `url` | 1 each |
| Space NK (`spacenk`) | `search`, `category`, `brand`, `brands`, `product`, `reviews`, `suggestions`, `stores`, `offers`; markets uk (default), ie, nl, au; `stores` UK only, by `product_id`; `offers` uk or ie | 1 each; a listing with `full=True` up to 5 |
| Lookfantastic (`lookfantastic`) | `search`, `list`, `product`, `suggestions`, `offers`, `brands`, `categories`; `market` (gb default, de, fr, es, it, nl, pl, at, ie, eu) and `currency` on every method; `list` takes `path` or `url`, `product` `sku` or `url` | 1 each |
| Cult Beauty (`cultbeauty`) | `search`, `list`, `product`, `suggestions`, `offers`, `brands`, `categories`; `market` gb (default) or intl and `currency` (12) on every method; no `offers` on intl | 1 each |
| YesStyle (`yesstyle`) | `search`, `category`, `brand`, `brands`, `deals`, `product`, `reviews`, `suggestions`, `markets`; `country` (39; 153 on `reviews` and `suggestions`) and `language`; `product` and `reviews` take `product_id` or `url` | listings and `product` 2 (`product` 3 with variants); the rest 1 |
| Notino (`notino`) | `search`, `product`, `reviews`, `category`, `brand`, `promo`, `brands`, `suggestions`, `stores`, `store`; `market` (27 storefronts, default de); `product` and `reviews` take `url` or `order_code` | 1 each (gb 2); a paged, sorted or filtered list 3 (gb 4) |
| Douglas (`douglas`) | `search`, `category`, `brand`, `deals`, `product`, `stores`, `store`, `review_summary`, `suggestions`, `brands`; `market` (15 storefronts, default de); `product` takes `code` or `url` | 1 each (2 on it) |
| Boots (`boots`) | `product`, `store_stock`, `stores`, `store`; `market` uk (default) or ie; no search: start from a product link | 1 each (2 on a second attempt) |
| Instacart (`instacart`) | `retailers` (start here), `search`, `cross_search`, `product`, `price_compare`, `categories`, `category`, `deals`, `stores`, `suggestions`, `reviews`; us (default) on every method; ca on every method except `cross_search` and `reviews`; `language="fr"` on ca (not `suggestions`) | 1 each; `search` 3 (2 when the page fits in the first answer); `cross_search` 3 up to 5 stores, 4 for 6 to 10 |
| Carrefour (`carrefour`) | `search`, `product`, `reviews`, `category`, `promotions`, `suggestions`, `stores`, `store_availability`, `store` | 1 each; `search` and `product` with `country="be"` 2 |
| Allegro (`allegro`) | `search`, `offer`, `product`, `product_offers`, `seller`, `seller_feedback`, `category` | 2 each |
| OLX (`olx`) | `search`, `offer`, `seller`, `seller_ads`, `filters`, `categories`, `locations`, `suggestions`, `similar` | 1 each |
| Trendyol (`trendyol`) | `search`, `product`, `category`, `brand`, `reviews`, `questions`, `seller`, `deals`, `coupons`, `rankings`, `suggestions`, `delivery`; 35 markets via `country` and `language` (`deals` and `coupons` tr only; `rankings` not on the English-language EU storefronts) | 1 each |
| Nintendo (`nintendo`) | `search`, `product`, `prices`, `deals`, `releases`, `dlc`; 46 countries via `country` and `language` (`prices` also kr, hk, tw and il) | 1 each |
| H&M (`hm`) | `search`, `product`, `stock`, `stores`, `category`, `deals`, `new_arrivals`, `suggestions`, `production`; 47 countries via `country` and `language` (`product` not on mo, tw or the shared EU store; `stores` not on mo) | `product` 2, the rest 1 each |
| Zara (`zara`) | `search`, `product`, `materials`, `stock`, `stores`, `store_stock`, `categories`, `category`, `deals`, `new_arrivals`, `prices`, `suggestions`; 102 storefronts via `country` and `language` (`stores` and `store_stock` not ao or iq, `new_arrivals` not dz, `suggestions` not on ad al am az ba dz mk mo uz xk) | billed what each call spent: 2 per call; `product` 2 to 6, `store_stock` 2 or 4, `deals` and `new_arrivals` 4, `prices` 2 per market that answered, `suggestions` 2 or 4; 1 per call on `cn` |
| ASOS (`asos`) | `search`, `product`, `stock`, `reviews`, `suggestions`, `category`, `categories`, `brands`, `deals`, `new_arrivals`, `markets`; 235 countries via `country` and `currency` (245 country-currency combinations; `suggestions` not on pl) | 1 each |
| Fashion Nova (`fashionnova`) | `search`, `product`, `collection`, `categories`, `suggestions`, `reviews`, `similar`; 104 countries via `country`, `language` en or es (es in 67; `categories`, `suggestions` and `reviews` global, `similar` US store) | 1 each |
| Mercari (`mercari`) | `search`, `item`, `category`, `categories`, `brands`, `brand`, `deals`, `trending`, `seller`, `seller_reviews`, `shop`; `country` us or jp (`deals` and `trending` us only; `seller`, `seller_reviews` and `shop` jp only) | 1 each |
| Depop (`depop`) | `search`, `product`, `category`, `brand`, `explore`, `suggestions`, `shop`, `shop_products`, `shop_sold`, `shop_reviews`, `shops_search`, `categories`, `brands`, `similar`; buyer markets us, gb, au, ie, ca, nz, de, fr, it via `country` (`similar` us only; shop data, `categories` and `brands` global) | `search`, `category`, `brand`, `explore` 1 (5 on nz); `product` 1 on us, 2 on gb au ie ca de fr it, 6 on nz; the rest 1 each |
| Poshmark (`poshmark`) | `search`, `sold`, `product`, `category`, `brand`, `closet`, `closet_listings`, `love_notes`, `closets_search`, `categories`, `brands`, `suggestions`, `parties`, `party_listings`, `similar`; `country` us or ca (`product`, closet endpoints and `categories` global) | 1 each |
| OfferUp (`offerup`) | `search`, `listing`, `category`, `categories`, `seller`; us only (no `country`); `search` and `category` take `zip` (required); `listing` takes `listing_id` or `url` | 1 each; `listing` 1, or 2 when it needs a second, costlier fetch |
| EstateSales.net (`estatesales`) | `sales`, `sale`, `companies`, `company`, `search`, `item`; US; `sales` by `zip`, or `city` with `state`; `companies` by `state` and metro; `sale`, `company` and `item` by id or `url` | 1 each |
| thredUP (`thredup`) | `search`, `sold`, `product`, `category`, `brand`, `deals`, `rescue_boxes`, `categories`, `brands`, `suggestions`, `trending`, `similar`; thredUP's US store (no `country`) | 1 each |
| bol.com (`bolcom`) | `search`, `product`, `offers`, `seller`, `seller_products`, `category`, `brand`, `deals`, `campaign`; storefronts nl-nl, be-nl, be-fr via `country` and `language` | 2 each; `product` by `ean` 4 |
| Kroger (`kroger`) | `search`, `product`, `prices`, `stores`, `category`, `deals`, `coupons`, `suggestions`; `banner` kroger, qfc or fred_meyer | `search` and `product` 2, `prices` 3, the rest 1 each |
| Publix (`publix`) | `search`, `product`, `category`, `categories`, `weekly_ad`, `extra_savings`, `coupons`, `savings_search`, `order_ahead`, `stores`, `suggestions`; `store_id` from `stores` | 1 each |
| IKEA (`ikea`) | `search`, `product`, `reviews`, `category`, `categories`, `deals`, `suggestions`, `stores`, `stock`, `items`, `compare`, `as_is`; 55 markets via `country` | 1 each; `compare` 1 per market that answered |
| Wayfair (`wayfair`) | `search`, `product`, `category`, `deals`; markets us, ca (en / fr), gb, ie via `country`; `site` allmodern, birchlane, jossandmain or perigold | 1 each |
| Ashley Furniture (`ashley`) | `search`, `product`, `category`, `deals`, `stores`, `store`; `search` and `product` also on ca, mx, ph, sa, tr via `country` (`product` by `handle` there) | `search` and `product` 2 on us and mx, 1 on ca, ph, sa, tr; the rest (us only) 2 each |
| Maisons du Monde (`maisonsdumonde`) | `search`, `product`, `category`, `deals`, `reviews`, `stores`, `store`, `availability`, `seller`; markets fr, be (fr / nl), lu, nl, de, es, it, pt, ch (fr / de / it) via `country` and `language` | 1 each |
| Trustpilot | `search`, `business`, `reviews`, `categories`, `category`, `review` | 2 each |
| Reclame Aqui (`reclameaqui`) | `company_search`, `company`, `complaints`, `complaint`, `complaint_search`, `rankings`, `segments`, `segment_ranking`; Brazil; `company` by `shortname` or `url`; `complaints` by `company_id` or `shortname`, filtered by status, category, product, problem and words; `complaint` by `url` or `company` + `complaint_id`; `segment_ranking` by `main_segment` + `segment` or `url` | 1 each, `complaints` by `shortname` 2 |
| Goodreads (`goodreads`) | `search`, `book`, `reviews`, `suggestions`, `author`, `author_books`, `series`, `editions`, `list`, `book_lists`, `list_search`, `quotes`, `genre`, `new_releases`; one global English site; `reviews` reads up to 4 pages of one view per call; `book` by `book_id`, `url` or `isbn` | 1 each |
| Barnes & Noble (`barnesandnoble`) | `search`, `product`, `store_availability`, `stores`, `store`, `suggestions`, `bestsellers`, `category`, `categories`, `deals`; US; `search` and `category` show 24 results; `product` by `ean` or `isbn`; `store_availability` takes `near` (a ZIP, a city or a store) and `ean` or `isbn`; `stores` by `near` or a point | 1 each |
| ThriftBooks (`thriftbooks`) | `search`, `isbn`, `work`, `edition`, `copies`, `editions`, `reviews`, `suggestions`; US; `search` by `query` or a `list` (bestsellers, deals, new_releases); `isbn` takes an ISBN-10 or ISBN-13; `work`, `editions` and `reviews` by `work_id`; `edition` and `copies` by `edition_id` | 1 each |
| Mercado Libre | `search`, `product`, `reviews`, `questions`, `best_sellers` | `reviews` 1, the rest 2 each |
| KaBuM! (`kabum`) | `search`, `category`, `categories`, `product`, `shipping`, `reviews`, `offers`; Brazil; `search` and `category` up to 100 a page with 5 sorts and facet `filters`; `product`, `shipping` and `reviews` by `product_id` or `url`; `shipping` takes a `cep`; `offers` by `campaign` (blackfriday or ofertaskabum) | 1 each |
| Magazine Luiza (`magalu`) | `search`, `category`, `deals`, `product`, `reviews`, `suggestions`, `stores`, `store`; Brazil; `search`, `category` and `deals` 40 a page, filtered by brand, seller, price, rating, Black Friday, promotion and attributes; `product` and `reviews` by `product_id` or `url`; `stores` by `state` (and `city`); `store` by `store_id` or `url` | 2 each |
| Casas Bahia (`casasbahia`) | `search`, `category`, `product`, `categories`; `site` casasbahia, extra or pontofrio; `search` and `category` 20 a page (list items carry no prices); `product` by `sku` or `url` with every seller's price | 2 each |
| Buscape (`buscape`) | `search`, `category`, `categories`, `product`, `offers`, `price_history`, `lowest_price`, `deals`, `deal_landing`, `store`, `suggestions`, `shipping`; `site` buscape or zoom; `offers`, `price_history`, `lowest_price` and `shipping` by `product_id`; `price_history` 40 days or 3-12 months; `shipping` takes `cep`, `state` and `city`; `store` by `store_id` or `store` | 1 each |
| Drogasil and Droga Raia (`rdsaude`) | `search`, `category`, `categories`, `product`, `prices`, `store_availability`, `stores`, `stores_search`, `reviews`, `deals`, `suggestions`; `site` drogasil or drogaraia; `search`, `category` and `deals` 24, 36 or 48 a page; `prices` up to 48 `skus`; `store_availability` up to 5 product x store checks; `stores` by `cep`, `stores_search` by state, city and services | 1 each |
| Leroy Merlin (`leroymerlin`) | `search`, `category`, `product`, `store_stock`, `stores`, `store`, `reviews`, `shipping`, `cep`, `regions`, `categories`, `suggestions`, `offers`; `country` br, it, es, pt, pl, ro or fr (no `search` on fr); Brazil needs `region` on priced calls; `store_stock`, `shipping`, `cep`, `regions` and `categories` Brazil only; `suggestions` it, es, pt, pl; `offers` it | billed per market: 1 in br, it, ro (it product and category 2), 2 in es, pt, pl, 5 in fr |
| Natura (`natura`) | `search`, `category`, `categories`, `product`, `suggestions`, `stores`, `deals`; `country` br, ar, cl, co, mx or pe (default br); listings up to 100 a page; `product` by `product_id` or `url`; `stores` Brazil only, by `state`, `city`, `cep` prefix and `type` | 1 each |
| O Boticario and Eudora (`boticario`) | `search`, `category`, `categories`, `deals`, `promotions`, `product`, `prices`, `reviews`, `stores`, `pickup`, `suggestions`; `brand` boticario or eudora; listings 36 a page; `product` and `pickup` by `slug`, `url` or `sku`; `prices` up to 10 `skus`; `stores` and `pickup` take a `cep` | 1 each; listings, `promotions` and `product` 2 when the page needs a second route; `prices` 1 per 5 SKUs |
| Centauro (`centauro`) | `search`, `category`, `deals`, `product`, `freight`, `stores`, `suggestions`; Brazil; listings 36 a page; `product` by `product_id`, `model` + `color` or `url`; `freight` takes a size `sku` and a `cep`; `stores` by `cep` | 1 each |
| ChatGPT | `prompt` | 5 per answered prompt |
| Gemini | `prompt` | 5 per answered prompt |
| Company (`company`) | `enrich` | 10 from a `url`, 20 from a `place_id` (1 when the listing has no readable website); unreachable site free |
| Extract (core, callable) | `client.extract(url)`, `extract.map`, `extract.crawl`, `extract.crawl_status`, `extract.cancel_crawl`, `extract.batch`, `extract.batch_status`, `extract.cancel_batch` | `extract`: 1 for `mode="normal"` or `"advanced"`, 2 for `"ultra"`, only on success. `map`: 1 on normal. `crawl` / `batch`: that same price per successful page. Status and cancel: free |

Every method's full parameter list is available inline in your editor (typed
keyword arguments with docstrings). See the [API docs](https://scavio.dev/docs?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
for field-level details.

### Changed in 0.102.0

- **7 new namespaces** (sync and async), 63 endpoints, Brazil: `kabum` (KaBuM!, 7),
  `magalu` (Magazine Luiza, 8), `casasbahia` (Casas Bahia, Extra and Ponto, 4),
  `buscape` (Buscape and Zoom, 12), `rdsaude` (Drogasil and Droga Raia, 11),
  `reclameaqui` (Reclame Aqui, 8) and `leroymerlin` (Leroy Merlin in Brazil, Italy,
  Spain, Portugal, Poland, Romania and France, 13). Credits: 1 per call except
  `magalu` and `casasbahia` (2), `reclameaqui.complaints` by `shortname` (2) and
  `leroymerlin`, billed per market (1 in Brazil, Italy and Romania, 2 in Spain,
  Portugal and Poland, 5 in France). The request timeout is raised to at least 240s.
- **3 more namespaces** (sync and async), 25 endpoints: `natura` (Natura in Brazil,
  Argentina, Chile, Colombia, Mexico and Peru, 7), `boticario` (O Boticario and Eudora,
  Brazil, 11) and `centauro` (Centauro, Brazil, 7). Credits: 1 per call; `boticario`
  listings, `promotions` and `product` 2 when the page needs a second route,
  `boticario.prices` 1 per 5 SKUs. The request timeout is raised to at least 240s.

### Changed in 0.101.0

- **5 new namespaces** (sync and async), 46 endpoints: `belk` (Belk, 10),
  `abercrombie` (Abercrombie & Fitch, abercrombie kids, Hollister and Gilly Hicks, 10),
  `llbean` (L.L.Bean, 11), `sweetwater` (Sweetwater, 6) and `bedbathbeyond` (Bed Bath
  & Beyond, 9). Credits: 1 per call except `belk` (2; `product` and `variant` up to 4,
  `store_availability` 1 plus 2 per looked-up variant), `abercrombie.reviews` without
  a `url` (2) and `bedbathbeyond` search, category and deal lists (2). The request
  timeout is raised to at least 240s.

### Changed in 0.100.0

- **5 new namespaces** (sync and async), 48 endpoints: `qvc` (QVC and HSN, 10),
  `barnesandnoble` (Barnes & Noble, 10), `thriftbooks` (ThriftBooks, 8), `uhaul`
  (U-Haul, 8) and `williamssonoma` (Williams Sonoma, Pottery Barn, West Elm and the
  other Williams-Sonoma, Inc. brands, 12). Credits: 1 per call except
  `williamssonoma.search` and `williamssonoma.category` (5). The request timeout is
  raised to at least 240s.

### Changed in 0.99.0

- **8 new namespaces** (sync and async), 72 endpoints, US retailers: `academy` (Academy
  Sports + Outdoors, 9), `bathandbodyworks` (Bath & Body Works, 10), `gap` (Gap Inc.:
  Gap, Old Navy, Banana Republic, Athleta and the factory stores, 11), `rakuten` (9),
  `bjs` (BJ's Wholesale Club, 7), `zappos` (Zappos and 6pm, 7), `newegg` (10) and `rei`
  (REI, 9). Credits: 1 per call except `newegg` and `rei` (2). The request timeout is
  raised to at least 240s.

### Changed in 0.98.0

- **11 new namespaces** (sync and async), 68 endpoints. Real estate: `movoto` (5),
  `hotpads` (HotPads, 5), `apartmentlist` (Apartment List, 6), `compass` (3),
  `affordablehousing` (AffordableHousing.com, 6), `lennar` (11). Self storage:
  `extraspace` (Extra Space Storage, 5), `publicstorage` (Public Storage, 3). Estate
  sales: `estatesales` (EstateSales.net, 6). Books: `goodreads` (14). Travel: `expedia`
  (4). Credits: 1 per call except `compass` (2), AffordableHousing.com `search` and
  `suggestions` (2) and `expedia` (billed on actual cost: 2, 1 on some pages). The
  request timeout is raised to at least 240s (`expedia` 250s).

### Changed in 0.97.0

- **8 new namespaces** (sync and async), 50 endpoints. Real estate: `rentcom` (Rent.com
  and Apartment Guide, 6), `trulia` (5), `streeteasy` (StreetEasy, 5), `rentcafe`
  (RentCafe, 6). Travel: `vrbo` (3). Cars: `truecar` (TrueCar, 9), `edmunds` (8), `kbb`
  (Kelley Blue Book, 8). Credits: 1 per call except `edmunds` (2), `vrbo` (billed on
  actual cost: 2 per attempt, a search 2 to 8) and Kelley Blue Book `car_value` at a
  `zip` (2, up to 6) and deeper `reviews` pages (up to 5). The request timeout is raised
  to at least 240s (`vrbo`, `edmunds` and `kbb` 250s).

### Changed in 0.96.0

- **14 new namespaces** (sync and async), 114 endpoints. Beauty: `spacenk` (Space NK, 9),
  `lookfantastic` (7), `cultbeauty` (Cult Beauty, 7), `yesstyle` (YesStyle, 9), `notino`
  (10), `douglas` (10), `boots` (4). Cars and parts: `rockauto` (RockAuto, 11), `carscom`
  (Cars.com, 8), `autotrader` (5), `cargurus` (CarGurus, 8), `carmax` (CarMax, 12),
  `carvana` (6), `bringatrailer` (Bring a Trailer, 8). Credits: 1 per call except
  `autotrader` (2), YesStyle listings and product (2; 3 with variants), Notino gb and
  paged lists, Douglas Italy and a Space NK `full=True` listing (up to 5). The request
  timeout is raised to at least 240s (Douglas and Notino `reviews` 250s).

### Changed in 0.95.0

- **New `pcexpress` namespace** (sync and async) for PC Express (Loblaw's
  online grocery for Real Canadian Superstore, No Frills, Loblaws, Zehrs,
  Fortinos, Valu-mart, Your Independent Grocer, Wholesale Club, Provigo and
  Maxi), 7 endpoints: `search`, `category`, `collection`, `product`,
  `stores`, `store`, `suggestions`. Prices in CAD at each banner's default
  store, deals with their end date and PC Optimum offer as shown, product
  GTIN and nutrition, pickup stores and store hours; `banner` (10) and
  `language` en or fr. Credits: `product` and `store` 5 (`product` 1 when it
  answers from the search listing), the rest 1. The request timeout is
  raised to at least 240s.

### Changed in 0.94.0

- **New `rona` namespace** (sync and async) for RONA (rona.ca, the Canadian
  home improvement retailer: RONA+ and RONA stores), 9 endpoints: `search`,
  `product`, `prices`, `category`, `categories`, `stores`, `store`, `stock`,
  `deals`. Store prices in CAD for up to 60 articles at one store with exact
  units, search, category and weekly deals priced at the store you choose, a
  product's sale end as RONA shows it, the 403 stores on RONA's store locator
  and which stores near a store have an article; `language` en or fr.
  Credits: `prices`, `categories`, `stores`, `store` 1; `search` and `deals`
  2 (3 with `store_id`); `product` and `stock` 3; `category` 1-3. The
  request timeout is raised to at least 240s.

### Changed in 0.93.0

- **Sephora Canada on `sephora`** (sync and async): `search`, `category` and
  `product` take `country="ca"` for Sephora Canada (sephora.com/ca, CAD), plus
  `language` (en or fr); `search` and `category` take `filters` and
  `include_facets`, and `category` takes `sort` for Canada. New Canada-only
  methods `brand`, `brands`, `suggestions`, `offers`, `stores` and `store`.
  Credits: 1 each, `product` and `offers` 2. US calls are unchanged: `country`
  is not sent unless you pass it, and US credits stay as they were. Every
  `sephora` call now raises the request timeout to at least 120 s (it never
  lowers a longer one), since Sephora Canada pages can take up to about 50 s.

### Changed in 0.92.0

- **Best Buy Canada on `best_buy`** (sync and async): all nine methods take
  `country="ca"` for Best Buy Canada (bestbuy.ca, CAD), plus `language` (en or
  fr) and `province` (the environmental handling fee); listings take
  `page_size`, `deals` takes `collection`, `stores` takes `postal_code`, `city`
  or `latitude` / `longitude`, and `availability` takes `postal_code` and
  `skus` (exact units per store). New Canada-only method `questions`. 1 credit
  per Canada call. US calls are unchanged: `country` is not sent unless you pass
  it, and US credits stay as they were. `stores`' `zip` is now optional
  (positional as before) because Canada searches by postal code, city or
  coordinates; one of them is required.

### Changed in 0.91.0

- **Home Depot Canada on `home_depot`** (sync and async): `search`, `product`
  and `reviews` take `country="ca"` for Home Depot Canada (homedepot.ca, CAD),
  plus `language` (en or fr), and `search` takes `store_id`, `category_id`,
  `page_size`, `filters`, `deals` and `include_facets`; `product` takes
  `store_id` for that store's price next to the online price. New methods
  `stores`, `availability` (both US and `country="ca"`) and `shipping` (US
  only; 2, 2 and 4 credits in the US, 1 for Canada). New Canada-only
  methods `category`, `categories`, `stock` (exact units at every store near a
  postal code or city), `store` and `suggestions`. 1 credit per Canada call.
  US calls are unchanged: `country` is not sent unless you pass it, and the US
  stays at 2 credits. `search`'s `query` is now optional (positional as
  before) because Canada also searches by `category_id` or `deals` alone; one
  of the three is required.

### Changed in 0.90.0

- **New `sportchek` and `marks` namespaces** (sync and async) for SportChek
  (sportchek.ca, Canada's sporting goods retailer) and Mark's (marks.com, the
  Canadian workwear, casual clothing and footwear retailer; L'Equipeur in
  French), both Canadian Tire Corporation banners, 8 endpoints each: `search`,
  `list`, `product`, `suggestions`, `store`, `brands`, `categories`, plus
  `reviews` (SportChek) and `questions` (Mark's). Prices in CAD with the was
  price, sale label and sale end date the site shows, variants with units at
  the assigned store and online, filters from the site's facets; Mark's
  `language="fr"` reads L'Equipeur. 1 credit per call. Answers take about
  10-90 seconds: the request timeout is raised to at least 240s.

### Changed in 0.89.0

- **New `offerup` namespace** (sync and async) for OfferUp (offerup.com,
  the US local marketplace for buying and selling used items, cars and
  trucks), 5 endpoints: `search`, `listing`, `category`, `categories`,
  `seller`. Asking prices around any US ZIP with the area OfferUp resolved,
  cars and trucks by dealer or private seller, make, model year and mileage,
  a listing's condition, posted date and vehicle details (no VIN), the
  category tree and a seller's public profile numbers. 1 credit per call;
  `listing` 1, or 2 when it needs a second, costlier fetch. The request
  timeout is raised to at least 240s.

### Changed in 0.88.0

- **New `dermstore` namespace** (sync and async) for Dermstore
  (dermstore.com, the US skincare and beauty retailer, shipping to the US and
  Canada), 7 endpoints: `search`, `list`, `product`, `suggestions`, `offers`,
  `brands`, `categories`. Price, RRP as Dermstore gives it and Dermstore's
  offer text per product and brand, variants with their own price and stock,
  UPC, auto-replenish plans, the 10 latest reviews, the current offers with
  their end times, and `country` `us` or `ca` (Dermstore's own CAD prices). 1
  credit per call. The request timeout is raised to at least 240s.

### Changed in 0.87.0

- **New `nellis` namespace** (sync and async) for Nellis Auction
  (nellisauction.com, the liquidation auction marketplace with pickup
  warehouses in Las Vegas, Phoenix, Houston, Philadelphia, Denver and Dallas),
  4 endpoints: `search`, `item`, `locations`, `categories`. Open auctions by
  shopping location (`location`) with the current bid, bid count and Nellis's
  own Estimated Retail Price, one lot by id (open, closed or sold) with a sold
  lot's final price and the bid history without bidder names, the 13 pickup
  warehouses with hours, and live category, brand and auction-event counts. 1
  credit per call. The request timeout is raised to at least 240s.

### Changed in 0.86.0

- **New `vevor` namespace** (sync and async) for VEVOR (vevor.com, the tools
  and equipment seller with storefronts in 13 countries), 11 endpoints:
  `search`, `product`, `shipping`, `reviews`, `questions`, `suggestions`,
  `categories`, `category`, `collections`, `deals`, `prices`. VEVOR's price
  on each storefront in its own currency (`country` + `language`), the was
  price only during a VEVOR deal with its start and end, variants with their
  own price and stock, the shipping fee and delivery date by US state or
  Canadian province, and the same SKU on all 13 storefronts in one call
  (`prices`, 3 credits). 1 credit per call otherwise. The request timeout is
  raised to at least 240s.

### Changed in 0.85.0

- **New `discounttire` namespace** (sync and async) for Discount Tire
  (discounttire.com, the US tire and wheel retailer, America's Tire in parts
  of CA, PA, NJ and NY), 15 endpoints: `search`, `vehicle`, `vehicle_tires`,
  `product`, `model`, `store_stock`, `stores`, `store`, `reviews`,
  `store_reviews`, `wheels`, `browse`, `categories`, `suggestions`,
  `appointments`. The price of a tire at a named store (`store` or `zip`),
  the vehicle fitment chain with original-equipment tires and staggered
  front / rear sets, exact units at the stores near a ZIP, tire and store
  reviews with full paging, and the read-only appointment calendar. 1 credit
  per call. The request timeout is raised to at least 240s.

### Changed in 0.84.1

- **`dollartree` docs follow the new response shape**: `split_case` is
  `{available, multiple}` (`fee` and `store_brand` removed), `product` adds
  `split_case_fee` and `banner_code`, and `store_stock` replaces
  `ship_to_home.units` with `max_order_units` and adds `dc_number`.

### Changed in 0.84.0

- **New `dollartree` namespace** (sync and async) for Dollar Tree
  (dollartree.com, the US and Canada discount variety store chain), 10
  endpoints: `search`, `product`, `category`, `categories`, `brand`, `deals`,
  `store_stock`, `stores`, `store`, `reviews`. Dollar Tree's online unit
  price next to its case price, case pack, minimum quantity and split-case
  rules, units of one item at a store plus its nearby stores, stores with
  hours and services, and the newest reviews with syndication flags. Canada
  store pages (`country="ca"`) on `store` only. 1 credit per call, `stores`
  5. The request timeout is raised to at least 240s, and to 300s on
  `store_stock`, `stores` and `reviews`.

### Changed in 0.83.0

- **New `staples` namespace** (sync and async) for Staples (staples.com, the
  US office supply retailer; Staples Canada at staples.ca), 12 endpoints:
  `search`, `product`, `category`, `categories`, `deals`, `coupons`,
  `store_stock`, `stores`, `store`, `reviews`, `questions`, `trending`.
  Staples' own price per unit and cost per page, page yield, promotions with
  their expiry, units of one item at the stores near a ZIP, reviews with full
  paging and customer Q&A. Canada (`country="ca"`, English or French) on
  `search` and `product`. 1 credit per call. The request timeout is raised to
  at least 240s on every endpoint.

### Changed in 0.82.0

- **New `nike` namespace** (sync and async) for Nike (nike.com, including
  Jordan Brand), 8 endpoints: `search`, `product`, `category`, `brand`,
  `deals`, `releases`, `release`, `reviews`. Nike's price next to its own full
  price and discount percent, every size with its GTIN, the launch calendar
  with a per-size level for launch items, and the same style code on 62
  storefronts in 42 countries (`country` + `language`). Lists are Nike's first
  page only. 1 credit per call. The request timeout is raised to at least 240s
  on every endpoint.

### Changed in 0.81.0

- **New `michaels` namespace** (sync and async) for Michaels (michaels.com),
  the US and Canada arts and crafts retailer, 11 endpoints: `search`,
  `product`, `store_stock`, `store_inventory`, `stores`, `store`, `category`,
  `categories`, `brand`, `deals`, `suggestions`. Units of one SKU at the stores
  near a ZIP or Canadian postal code as Michaels reports them, units of up to
  30 SKUs at one store, a product with every variant's price and UPC, Michaels'
  own Reg. label and offer dates, online stock, the category tree, brands and
  deals. `country` us or ca, `language` en or fr (ca). 2 credits per call
  (`category` and `deals` 4 with a `/shop/` category). The request timeout is
  raised to at least 240s on every endpoint.

### Changed in 0.80.0

- **New `tractorsupply` namespace** (sync and async) for Tractor Supply
  (tractorsupply.com), the US rural lifestyle retailer, 12 endpoints:
  `search`, `product`, `store_prices`, `store_stock`, `fulfillment`, `stores`,
  `store`, `category`, `categories`, `brand`, `deals`, `promotions`. An item's
  price at the store you pick (`store` or `zip`, named in `priced_for` with the
  store's price zone), one item's price at up to 25 stores in one call, exact
  units per store with in-transit stock and its pickup date, pickup and
  delivery options for a ZIP, stores near a ZIP, the category tree, brands,
  deals and an item's promotions with dates. US only; no method takes
  `country`. The request timeout is raised to at least 240s on every endpoint.

### Changed in 0.79.0

- **New `acehardware` namespace** (sync and async) for Ace Hardware
  (acehardware.com), the US hardware cooperative, 11 endpoints: `search`,
  `product`, `store_stock`, `store`, `stores`, `category`, `categories`,
  `brand`, `deals`, `weekly_ad`, `paint_colors`. An item's price for the Ace
  store you pick (`product` with `store`, named in `priced_for`), exact units
  on hand at up to 25 stores or at one store and its 25 nearest, store details
  and the 25 nearest stores, each store's weekly ad with valid dates, deals
  with promo codes, the category tree, brands and Ace's paint colours. US only;
  no method takes `country`. The request timeout is raised to at least 240s on
  every endpoint.

### Changed in 0.78.0

- **New `oreilly` namespace** (sync and async) for O'Reilly Auto Parts
  (oreillyauto.com), the US auto parts retailer, 14 endpoints: `search`,
  `cross_reference`, `product`, `vehicles`, `compatibility`, `category`,
  `categories`, `brand`, `store_stock`, `stores`, `store`, `suggestions`,
  `rebates`, `deals`. Part-number cross-reference (another brand's or an OE
  number to O'Reilly's parts), parts that fit a vehicle (`base_vehicle_id`),
  VIN decode, price, sale price, core charge and rebates for the store O'Reilly
  prices the request for (`priced_for`), store stock near a ZIP (availability
  states), stores near a ZIP and the store directory (us and mx), rebates and
  deals. 2 credits per call (4 or 6 where the request needs more lookups).
  240s timeout floor.

### Changed in 0.77.0

- **New `instacart` namespace** (sync and async) for Instacart
  (instacart.com), the US and Canada grocery delivery and pickup marketplace,
  11 endpoints: `retailers`, `search`, `cross_search`, `product`,
  `price_compare`, `categories`, `category`, `deals`, `stores`,
  `suggestions`, `reviews`. Instacart prices by store at a ZIP: every store
  serving a ZIP with its pricing label, one product priced at every store,
  one query across up to 10 stores, delivery, pickup or in-store prices
  (`service_type`), each answer naming the store, ZIP and service type in
  `priced_for`. us and ca (CAD; `language="fr"` for French). 1 credit per
  call, `search` 3 (2 when the page fits in the first answer),
  `cross_search` 3-4. 240s timeout floor.

### Changed in 0.76.0

- **New `autozone` namespace** (sync and async) for AutoZone (autozone.com),
  the US auto parts retailer, 12 endpoints: `search`, `product`, `category`,
  `brand`, `vehicles`, `reviews`, `stores`, `store`, `categories`,
  `clearance`, `rebates`, `store_stock`. Parts that fit a year / make / model,
  part-number cross-reference, price, was price, deal price, core charge and
  warranty for the store AutoZone prices the request for (`priced_for`),
  reviews, the store directory, clearance and mail-in rebates; Brazil search,
  product and store stock at a chosen store; Mexico vehicles, stores and
  categories. 1 credit per call, 2 on br search / product and store_stock.
  240s timeout floor.

### Changed in 0.75.0

- **New `hema` namespace** (sync and async) for HEMA (hema.com), the Dutch
  variety store, 13 endpoints: `search`, `product`, `category`, `categories`,
  `new_arrivals`, `sale`, `offers`, `campaign`, `suggestions`, `store_stock`,
  `stores`, `store`, `reviews`. Webshops nl, be (nl or fr), fr and de; stores
  also in lu and at. HEMA store stock (sellable units and stock level per
  store for up to 12 articles near a city or postcode), each article's dated
  price schedule with upcoming promotions, weekly offers, Christmas and
  Sinterklaas campaigns and HEMA's own reviews. 1 credit per call. 240s
  timeout floor.

### Changed in 0.74.0

- **New `action` namespace** (sync and async) for Action (action.com), the
  European non-food discount store, 16 endpoints: `search`, `product`,
  `products`, `category`, `categories`, `brand`, `brands`, `new_arrivals`,
  `weekly_deals`, `collection`, `suggestions`, `stores`, `store`, `reviews`,
  `webshop_search`, `webshop_product`. 19 storefronts in 16 countries
  (`country` + `language`); this week's deals with Action's week id and
  validity dates; up to 60 article numbers priced on one market per call; the
  20 stores nearest a city or postcode with opening hours (Action does not
  publish store stock). 1 credit per call. 240s timeout floor.

### Changed in 0.73.0

- **New `mediaexpert` namespace** (sync and async) for Media Expert
  (mediaexpert.pl, Poland, PLN), 13 endpoints: `search`, `product`,
  `store_stock`, `stores`, `reviews`, `category`, `categories`, `brands`,
  `brand`, `promotions`, `outlet`, `seller`, `suggestions`. Price, old
  price, the Omnibus 30-day low Media Expert shows and the code price with
  its code and dates; Media Expert's stock indicator (not unit counts) at the
  40 stores nearest a Polish city or postcode; reviews up to 100 per page.
  Billed on actual cost, 1 to 3 credits per call. 240s timeout floor.
- **`argos`** docstrings: review `stats` no longer lists `brand`; Trusted
  Seller items' delivery fields are `None` (the seller sets delivery).

### Changed in 0.72.1

- **`argos`** docstrings: delivery `later` is Argos's "Delivery within N
  days" with the new `days` field; `total_capped` on search, category and
  deals (Argos stops counting at 10,000); store types defined (a collection
  point is collect-only, `inside_sainsburys` an Argos counter in a
  Sainsbury's store); product `rating` is `None` without reviews; one badge
  entry per code; phones as `+44...`; a postcode that does not exist ends in
  an unbilled 502 after about 50 seconds. Trusted Seller items: `free_delivery`
  and `delivery_cost` (lists) and `delivery_price` / `free_delivery`
  (product) are `None` (the seller sets delivery; Argos shows no charge).

### Changed in 0.72.0

- **New `argos` namespace** (sync and async) for Argos (argos.co.uk, UK,
  GBP), 10 endpoints: `search`, `product`, `store_stock`, `stores`,
  `reviews`, `questions`, `categories`, `category`, `deals`, `suggestions`.
  Store stock near a UK postcode as collection and delivery states (no unit
  counts), price, was price, offers and badges, reviews up to 100 per page.
  2 credits each. 240s timeout floor.

### Changed in 0.71.1

- **`fashionnova`**: `collection` pages 1 to 166 (a collection lists up to
  about 10,000 products); new `code_lowers_price` field on items and
  products (`price_with_code` is 40% off the compare-at price and can be at or
  above `price`); docstrings note per-style reviews, approximate
  `total_pages`, page repeats and the vendor `brand` field.

### Changed in 0.71.0

- **New `fashionnova` namespace** (sync and async) for Fashion Nova, 7
  endpoints: `search`, `product`, `collection`, `categories`, `suggestions`,
  `reviews`, `similar`. 104 countries via `country` (local currency) and
  `language` (`en`, or `es` in 67 countries): price, compare-at price, percent
  off, final sale and per-size stock. 1 credit each. 240s timeout floor.

### Changed in 0.70.0

- **New `thredup` namespace** (sync and async) for thredUP, 12 endpoints:
  `search`, `sold`, `product`, `category`, `brand`, `deals`,
  `rescue_boxes`, `categories`, `brands`, `suggestions`, `trending`,
  `similar`. thredUP's US store (USD), no `country` param. Sold listings
  by brand or category with no sold date. 1 credit each. 240s timeout floor.

### Changed in 0.69.0

- **New `poshmark` namespace** (sync and async) for Poshmark, 15 endpoints:
  `search`, `sold`, `product`, `category`, `brand`, `closet`,
  `closet_listings`, `love_notes`, `closets_search`, `categories`,
  `brands`, `suggestions`, `parties`, `party_listings`, `similar`.
  Markets us (default, USD) and ca (CAD) via `country`; listing ids and
  closets are global. Sold search up to 480 per query and filter
  combination. 1 credit each. 240s timeout floor.

### Changed in 0.68.1

- `depop` docstrings: list items carry `buyer_market_price` and no seller country (`product` has `seller.country`); `shop_sold` status `sold` or `marked_as_sold`; price wording (`total` is Scavio's sum, `headline_price` Depop's own headline).

### Changed in 0.68.0

- **New `depop` namespace** (sync and async) for Depop, 14 endpoints:
  `search`, `product`, `category`, `brand`, `explore`, `suggestions`,
  `shop`, `shop_products`, `shop_sold`, `shop_reviews`, `shops_search`,
  `categories`, `brands`, `similar`. Buyer markets us (default), gb, au,
  ie, ca, nz, de, fr, it via `country`; shop data, `categories` and
  `brands` are global, `similar` us only. `search`, `category`, `brand`,
  `explore` 1 credit (5 on nz); `product` 1 on us, 2 on gb au ie ca de fr
  it, 6 on nz; the rest 1. 240s timeout floor.

### Changed in 0.66.0

- **New `bolcom` namespace** (sync and async) for bol.com (the Netherlands
  and Belgium), 9 endpoints: `search`, `product`, `offers`, `seller`,
  `seller_products`, `category`, `brand`, `deals`, `campaign`. Storefronts
  nl-nl (default), be-nl and be-fr via `country` and `language`;
  `product_id` is a string. 2 credits each, `product` by `ean` 4. 240s
  timeout floor. `offers` returns the 10 lowest-priced offers with counts by
  condition for all (`has_more`, no paging); listing pages run 1 to 500.

### Changed in 0.65.0

- **New `mercari` namespace** (sync and async) for Mercari US and Mercari
  Japan, 11 endpoints: `search`, `item`, `category`, `categories`,
  `brands`, `brand`, `deals`, `trending`, `seller`, `seller_reviews`,
  `shop`. `country` us (default) or jp; `search` with `status="sold"`
  returns sold listings with their prices. 1 credit each. 240s timeout
  floor.

### Changed in 0.64.0

- **New `asos` namespace** (sync and async) for ASOS, 11 endpoints:
  `search`, `product`, `stock`, `reviews`, `suggestions`, `category`,
  `categories`, `brands`, `deals`, `new_arrivals`, `markets`. 235
  countries via `country` and `currency` (245 combinations); `stock` takes
  up to 100 product ids per call. 1 credit each. 120s timeout floor.

### Changed in 0.63.0

- **New `zara` namespace** (sync and async) for Zara, 12 endpoints:
  `search`, `product`, `materials`, `stock`, `stores`, `store_stock`,
  `categories`, `category`, `deals`, `new_arrivals`, `prices`,
  `suggestions`. 102 storefronts via `country` and `language`; `prices`
  compares one reference across up to 10 markets per call. Billed what each
  call spent (`credits_used`). 120s timeout floor.

### Changed in 0.62.0

- **New `hm` namespace** (sync and async) for H&M, 9 endpoints: `search`,
  `product` (2 credits), `stock`, `stores`, `category`, `deals`,
  `new_arrivals`, `suggestions`, `production` (1 credit each). 47 countries
  via `country` and `language`; `product` not on mo, tw or the shared EU
  store, `stores` not on mo. Article codes are the same in every market.
  120s timeout floor.

### Changed in 0.61.0

- **New `nintendo` namespace** (sync and async) for the Nintendo eShop, 6
  endpoints at 1 credit each: `search`, `product`, `prices`, `deals`,
  `releases`, `dlc`. 46 countries via `country` and `language` (`prices` also
  kr, hk, tw and il). Item ids are per eShop region; `prices` takes 1 to 50
  ids. 120s timeout floor.

### Changed in 0.60.1

- `trendyol` docstrings: international storefronts are sold by Trendyol itself
  or by other sellers (check `buy_box` and `other_sellers`); the earlier
  "mostly sold by Trendyol" wording is removed. No code change.

### Changed in 0.60.0

- **New `trendyol` namespace** (sync and async) for Trendyol, 12 endpoints at
  1 credit each: `search`, `product`, `category`, `brand`, `reviews`,
  `questions`, `seller`, `deals`, `coupons`, `rankings`, `suggestions`,
  `delivery`. 35 markets via `country` and `language`; `deals` and `coupons`
  tr only; `rankings` not on the 15 English-language EU storefronts.
  `product` returns the buy box and every other seller's offer. 120s timeout
  floor.

### Changed in 0.59.0

- **New `maisonsdumonde` namespace** (sync and async) for Maisons du Monde, 9
  endpoints at 1 credit each: `search`, `product`, `category`, `deals`,
  `reviews`, `stores`, `store`, `availability`, `seller`. Markets fr, be (fr /
  nl), lu, nl, de, es, it, pt (EUR) and ch (fr / de / it, CHF) via `country`
  and `language`; stores and store stock on fr, be, de, es, it, pt and ch;
  marketplace sellers on fr, de, es and it. 120s timeout floor.

### Changed in 0.58.0

- **New `ashley` namespace** (sync and async) for Ashley Furniture, 6
  endpoints: `search`, `product`, `category`, `deals`, `stores`, `store`.
  `search` and `product` also serve Ashley's licensed storefronts (ca, mx, ph,
  sa, tr; `product` by `handle` there) and cost 2 credits on us and mx, 1 on
  the rest; the other four are us only at 2 credits. Every us answer carries
  `priced_for` (the ZIP and price zone it was priced for). 120s timeout floor.

### Changed in 0.57.0

- **New `wayfair` namespace** (sync and async) for Wayfair (us, ca en / fr,
  gb, ie; AllModern, Birch Lane, Joss & Main and Perigold via `site`), 4
  endpoints at 1 credit each: `search`, `product`, `category`, `deals`.
  `product` takes `option_id` for one option's price and stock and `zip` for
  a delivery estimate (us, ca). 120s timeout floor.

### Changed in 0.56.0

- **New `ikea` namespace** (sync and async) for IKEA across 55 markets, 12
  endpoints at 1 credit each: `search`, `product`, `reviews`, `category`,
  `categories`, `deals`, `suggestions`, `stores`, `stock`, `items`,
  `compare` (1 credit per market that answered), `as_is`. `country` picks the
  market, `language` one of its languages. 180s timeout floor on `product`
  and `reviews`, 120s elsewhere.

### Changed in 0.55.0

- **New `publix` namespace** (sync and async) for Publix (publix.com, US),
  11 endpoints at 1 credit each: `search`, `product`, `category`,
  `categories`, `weekly_ad`, `extra_savings`, `coupons`, `savings_search`,
  `order_ahead`, `stores`, `suggestions`. Store-scoped: `store_id` (a Publix
  store number from `stores()`) on every price endpoint. 120s timeout floor.

### Changed in 0.54.0

- **`kroger` namespace: QFC and Fred Meyer, 6 new endpoints.** Every method
  takes `banner` (`kroger` default, `qfc`, `fred_meyer`). New: `prices`
  (up to 25 UPCs at one store you choose, 3 credits), `stores`, `category`,
  `deals` (weekly digital deals), `coupons` (listed, not clipped) and
  `suggestions`, 1 credit each. `search` and `product` now also return
  `banner` and the `store` that priced them; `search` serves page 1 only
  (`page` above 1 is an unbilled 400). 120s timeout floor.

### Changed in 0.53.0

- **New `olx` namespace** (sync and async) for OLX Europe, 9 endpoints at
  1 credit each: `search`, `offer`, `seller`, `seller_ads`, `filters`,
  `categories`, `locations`, `suggestions`, `similar`. `country` pl
  (default), ro, pt, bg, ua, kz or uz (`filters` and `similar`: pl, ro, pt,
  bg, ua); `language` (kk on kz, uz on uz, ru on both) on `search`,
  `seller_ads` and `offer`. 120s timeout floor.

### Changed in 0.52.0

- **New `company` namespace** (sync and async) with `enrich(url=None,
  place_id=None)`: a business's published emails, phones, socials, contact
  page and owner from its website or a Google Maps place_id. One of `url` or
  `place_id` is required. 10 credits from a url, 20 from a place_id. 180s
  timeout floor.

### Changed in 0.51.0

- **New `allegro` namespace** (sync and async) for Allegro, 7 endpoints at
  2 credits each: `search`, `offer`, `product`, `product_offers`, `seller`,
  `seller_feedback`, `category`. Every endpoint takes `country` pl
  (default), cz, sk or hu; `buying_format` and `deals` are pl only. 120s
  timeout floor.

### Changed in 0.50.0

- **New `carrefour` namespace** (sync and async) for Carrefour, 9 endpoints
  at 1 credit each: `search`, `product`, `reviews`, `category`,
  `promotions`, `suggestions`, `stores`, `store_availability`, `store`.
  carrefour.fr serves every endpoint; `search` and `product` also take
  `country` ar, ro or be (`language` fr or nl; 2 credits on be). `store`
  scopes prices and assortment to one store. 120s timeout floor.

### Changed in 0.49.1

- `fanatics` docstrings: price sorts order by the current `price`, not the
  with-code price; department and filter ids are per store; the players
  facet appears only on some pages; `price_label` `coupon` means
  coupon-eligible; product `on_sale` covers clearance markdowns.

### Changed in 0.49.0

- **New `fanatics` namespace** (sync and async) for Fanatics merchandise,
  5 endpoints at 1 credit each: `search`, `product`, `browse`, `deals`,
  `reviews`. `country` picks one of 8 storefronts (us default, gb, de, fr,
  es, it, jp, ca), `language` the ca language and `site` a US league store
  (nflshop, mlbshop, nhlshop, mlsstore); `reviews` is US only. 120s timeout
  floor, 300s for `reviews`.

### Changed in 0.48.0

- **New `footlocker` namespace** (sync and async) for Foot Locker, 10
  endpoints at 1 credit each: `search`, `product`, `category`, `brand`,
  `deals`, `releases`, `stores`, `store_availability`, `reviews`,
  `questions`. `country` picks one of 13 storefronts (us default, ca, gb,
  de, fr, it, es, nl, be, at, ie, au, nz) and `language` the ca / be
  language; `releases` covers us, ca and gb and takes `date_from` /
  `date_to`; `stores`, `store_availability`, `reviews` and `questions` are
  US only. 120s timeout floor, 240s for `reviews` and `questions`.

### Changed in 0.47.0

- **New `dicks` namespace** (sync and async) for dickssportinggoods.com
  (Dick's Sporting Goods, US, USD), 9 endpoints: `search`, `product`,
  `products`, `reviews`, `category`, `brand`, `deals`,
  `store_availability`, `suggestions`, 1 credit each except `product` and
  `reviews` (2). The grid endpoints take `brand`, `page_size` (up to 144),
  a `sort`, `min_price` / `max_price` and any facet via `filters` (a dict);
  `product` returns per-SKU prices and online units; `products` takes up to
  5 `product_ids`; `store_availability` takes a list of `skus` and an
  optional `chain` (Golf Galaxy, Public Lands). 120s timeout floor, 240s
  for `product` and `reviews`.

### Changed in 0.46.0

- **`jcpenney.reviews` and `jcpenney.questions`** (sync and async), 1 credit
  each, taking `product_id` or `url`. `reviews` returns review text (up to
  98, `sort`, one-star `rating` filter, `max_reviews`) with `total_reviews`,
  `displayed_reviews` and `matching_reviews`; `questions` returns questions
  and every answer with `author_type` and `ai_label` (up to 50,
  `max_questions`). Both raise the request timeout to at least 240s: they
  usually take 15-90s, up to about 3 minutes.

### Changed in 0.45.0

- **New `jcpenney` namespace** (sync and async) for jcpenney.com (US incl.
  Puerto Rico stores, USD), 9 endpoints at 1 credit each: `search`,
  `product`, `category`, `brand`, `deals`, `stores`, `store_availability`,
  `suggestions`, `coupons`. The grid endpoints take `brand`, `color`,
  `size`, `price_range`, `deal` (one value or a list), a `sort` and any
  facet via `filters` (a dict); `product` takes up to 20 `product_ids`;
  `store_availability` takes a required `sku` and returns unit counts at the
  5 nearest stores. 120s timeout floor on every method.

### Changed in 0.44.0

- **New `kohls` namespace** (sync and async) for kohls.com (US, USD), 9
  endpoints: `search`, `product`, `category`, `brand`, `deals`, `stores`,
  `store_availability`, `suggestions`, `coupons`. 2 credits each, `stores`
  1. The grid endpoints take `brand`, `color`, `size`, `on_sale`,
  `clearance`, a `sort` (incl. `percent_off`, `highest_rated`) and facet
  value ids via `filters` (one or a list); `store_availability` takes a
  required `sku` and `zip`. 120s timeout floor on every method.

### Changed in 0.43.0

- **New `saks` namespace** (sync and async) for saksfifthavenue.com (US,
  USD), 9 endpoints at 2 credits each: `search`, `product`, `category`,
  `brand`, `deals`, `stores`, `store_availability`, `suggestions`,
  `designers`. The grid endpoints take `brand`, `color`, `size`, a price
  range, `on_sale`, `new_arrivals`, any facet via `filters` (a dict) and
  `start` / `page` paging; `store_availability` takes a required variant
  `sku`. 120s timeout floor on every method.

### Changed in 0.42.0

- **New `macys` namespace** (sync and async) for macys.com (US, USD), 9
  endpoints at 1 credit each: `search`, `product`, `reviews`, `category`,
  `brand`, `deals`, `stores`, `store_availability`, `suggestions`. The grid
  endpoints take `brand`, `color`, `special_offer`, a price range,
  `pickup_store_id`, any facet via `filters` (a dict) and
  `include_sponsored`; `product` takes up to 10 `product_ids` in one call.
  120s timeout floor on every method.

### Changed in 0.41.1

- **`vinted`:** the `country` docs now say what Vinted actually does: every
  site, `uk`, `us` and `au` included, can show listings from sellers in other
  countries, priced in the site's currency, and `product` returns the seller's
  own price and currency. `filters(category_id=...)` now narrows the options
  to that category (a server-side fix; no SDK signature change).

### Changed in 0.41.0

- **New `vinted` namespace** (sync and async) for Vinted on 27 country sites
  (`country`, `fr` default), 9 endpoints at 1 credit each: `search`,
  `product`, `seller`, `seller_products`, `seller_feedback`, `brands`,
  `suggestions`, `filters`, `categories`. `search` and `seller_products`
  return the price, the Vinted fee (`service_fee`) and `total_price`; the id
  filters (`brand_ids`, `status_ids`, `size_ids`, `color_ids`,
  `material_ids`) take a list or a comma-separated string. 120s timeout floor
  on every method.

### Changed in 0.40.0

- **New `tcgplayer` namespace** (sync and async) for tcgplayer.com (US, USD),
  13 endpoints at 1 credit each: `search`, `product`, `listings`,
  `price_history`, `sales`, `games`, `sets`, `price_guide`, `suggestions`,
  `trending`, `seller`, `seller_feedback`, `seller_products`. `product`
  returns the market price per SKU (condition x printing x language) with the
  recent sale range; `price_history` returns up to a year of sold volume per
  SKU. 120s timeout floor on every method.

### Changed in 0.39.0

- **New `best_buy` namespace** (sync and async) for bestbuy.com (US):
  `search`, `product`, `reviews`, `category`, `deals`, `stores`,
  `availability`, `suggestions`, `prices`. `product` returns open-box offers
  by condition (fair, good, excellent) with savings against new and regular;
  `availability` returns per-store pickup status at up to 8 stores; `prices`
  takes up to 15 SKUs per call. 120s timeout floor on every method.

### Changed in 0.38.0

- **New `nordstrom_rack` namespace** (sync and async) for nordstromrack.com
  (US): `search`, `category`, `brand`, `product`, `reviews`, `availability`,
  `stores`, `suggestions`, with the same parameters, credits (5 each,
  `availability` and `reviews` 10) and timeout floors (120s, `reviews` 150s)
  as `nordstrom`. `category` takes `/shop` and `/clearance` paths, including
  Clear the Rack and flash events (`/shop/flash/event-N`); `brand` takes
  `/brands/<slug>`. Product and listing rows carry `clearance_price_range`,
  `promotion_price_range` and `promotion_percent_off`.

### Changed in 0.37.0

- `nordstrom.reviews(*, url, style_id, sort, stars, verified_only, with_photos,
  search, max_reviews)` (sync and async), 10 credits: a product's full review
  history, up to 200 per call (default 60), sorted `most_helpful` (default),
  `most_recent`, `highest_rated` or `lowest_rated`, filtered by star ratings,
  verified purchases, photos or a text search (`search` cannot be combined
  with `sort`). Returns the review summary (average, histogram, size and width
  rating, praised and criticized features with a quote, rating-only count),
  the AI review summary, `total_results`, `returned` and `has_more`. Calls take
  20-60s (up to about 100s at 200 reviews), so this method's timeout floor is
  150s.

### Changed in 0.36.0

- `nordstrom` gains five methods (sync and async), all with the 120s timeout floor:
  - `category(category, *, page, sort)`, 5 credits: a /browse category path or
    URL (departments, `sale/women`, `/browse/new`), 24 products a page plus the
    category's breadcrumbs, subcategories and the filter sidebar with counts.
  - `brand(brand, *, page, sort)`, 5 credits: a /brands path or URL (a product's
    `brand_url` works), same rows and filters.
  - `stores(*, zip, latitude, longitude, store_numbers, distance_miles)`, 5
    credits: pass exactly one of `zip`, `latitude` + `longitude`, or
    `store_numbers` (list or comma-separated string); radius 1-100 miles,
    default 100.
  - `availability(*, url, style_id, sku_id)`, 10 credits: per sku ship
    quantity, pickup quantity (chain-wide) and the stores that can do pickup.
  - `suggestions(query, *, limit)`, 5 credits: search-box autocomplete, 1-20,
    default 8.

### Changed in 0.35.0

- **New `nordstrom` namespace** (sync and async), 5 credits per call.
  - `search(query, *, page, sort)`: nordstrom.com (US), 24 products a page.
    `sort`: relevance, rating, price_high, price_low, newest, percent_off.
  - `product(*, url, style_id)`: pass one. Every color and size as a sku with
    sku id, UPC, price, original price, percent off, price type, in_stock and
    quantity available to ship; star histogram, size-fit distribution and the
    reviews shown on the product page.
  - Both raise the request timeout to 120s.

### Changed in 0.34.0

- `menards.search(query, store_id, ...)` (sync and async), 2 credits: menards.com
  search at one store, 40 products a page, with price, sale price, the mail-in
  rebate, final price and that store's stock count. `sort` (relevance,
  price_asc, price_desc, brand_asc, brand_desc; price sorts use the everyday
  price), `in_stock_today`, `min_price`, `max_price`, `page`. An unknown store
  number is a 400.

### Changed in 0.33.0

- **Seven new US retail namespaces, 33 methods** (sync and async).
  - `whole_foods`: `search`, `category`, `deals`, `product`, `stores`, `store`,
    `sales_flyer` (1 credit each). Prices are one store's (5-digit `store_id`,
    default 10145): regular, sale and Prime member price. `product` returns the
    in-store and online price as separate blocks. Search sorts by relevance or
    price only.
  - `harbor_freight`: `search`, `clearance`, `product`, `prices` (up to 50
    item numbers), `stores`, `availability`, `reviews` (1 each). National
    prices with sale end date, coupon, Inside Track Club member price and
    compare-at. Store stock is a status plus aisle from a daily snapshot.
  - `petsmart`: `search`, `product`, `stores`, `store_stock`, `availability`,
    `deals` (1 each). Autoship first-order and recurring prices; stock is a unit
    count per store. `availability` takes `pairs` of `{"store_id", "sku"}`.
  - `petco`: `search`, `category`, `product`, `stores`, `store_inventory` (1
    each). `store_inventory` takes `cat_entry_ids`, not part numbers.
    `category` and `product` can take 10-30 seconds, so their request timeout
    is raised to 120s.
  - `iherb`: `search`, `product`, `prices` (up to 50 ids), `reviews` (2 each).
    Online only, US/USD; `reviews` is the rating summary and histogram with the
    top positive and top critical review.
  - `chewy`: `search`, `product` (10 each). One-time, Autoship and
    first-Autoship prices and MAP fields; `search` reports a category redirect.
  - `menards`: `product`, `stores` (1 each; `product` with `store_id` 2, adds
    stock quantity and aisle). No search. `product` timeout raised to 120s.

### Changed in 0.32.1

- `cvs.search`: `same_day_delivery` is now always `None`, as on `cvs.stock`. CVS
  reports one same-day count per SKU whichever store is sent, so it was not the
  store's number.

### Changed in 0.32.0

- **Six new US retail namespaces, 20 methods** (sync and async).
  - `sephora`: `search`, `category`, `product` (1 credit each). `product` takes
    `url` or `product_id` and returns a review summary with pro/con sentiment
    counts (no review text).
  - `ulta`: `search`, `category`, `product`, `stores` (1 each). `stores` is in
    stock / out of stock for one shade at the 10 stores nearest a ZIP.
  - `aldi`: `search`, `product`, `stores` (1 each). Pass `store_id` or `zip`;
    `service_type` picks the in-store (default), pickup or delivery price.
  - `micro_center`: `search`, `product` (2 each), `stores` (1). Stock is per
    3-digit `store_id` (web store 029 when omitted), capped at 25+.
  - `walgreens`: `search`, `product`, `stores` (2 each), `stock` (4, up to 20
    stores). Prices are national.
  - `cvs`: `search`, `product`, `stock` (1 each, `stock` up to 20 SKUs). No
    store locator; `search` defaults to store 7019. `product` can take 10-30+
    seconds, so its request timeout is raised to 120s.

### Changed in 0.31.0

- **Four new store-level retail namespaces, 21 methods** (sync and async). Every
  method answers for one store or club you choose.
  - `lowes`: `search`, `product`, `stores` (2 credits each), `reviews` (1).
    `store_id` and the store's `zip` are required on `search` and `product`;
    `search(on_sale=True)` returns that store's deals.
  - `sams_club`: `search`, `product`, `clubs`, `savings`, `category`, `reviews`
    (1 each). `product(club_id=...)` prices and stocks one club; clearance is
    `category("1150109")`.
  - `canadian_tire`: `search`, `product`, `stores`, `availability` (up to 50
    SKUs), `clearance`, `deals` (1 each). `store_id` is required except on
    `stores`.
  - `dollar_general`: `search`, `product`, `stores` (pass `upc` for per-store
    unit counts at up to 25 stores), `deals` (`on_sale` or `clearance`),
    `coupons` (1 each).

### Changed in 0.27.0

- **New `target.availability(tcin, zip, radius=None, store_id=None)`.** In-store
  stock for one product at every Target store near a 5-digit US ZIP: units,
  in-store, pickup, curbside and ship-to-store status, distance, address and
  hours, up to 20 stores. `store_id` narrows the result to one store. 1 credit.

  ```python
  stock = client.target.availability("85978609", "79407")
  for s in stock["data"]["stores"]:
      print(s["store_id"], s["name"], s["quantity"], s["in_store"], s["pickup"])
  ```
- `store_id` on `target.search`, `category`, `product` and `reviews` sets the
  store for prices only; its docstring no longer mentions availability. No
  behaviour change.

### Changed in 0.26.2

- `chatgpt.prompt` now costs 2 credits per answered prompt. Gemini stays at 5.

### Changed in 0.26.1

- `chatgpt.prompt` now costs 1 credit per answered prompt (was 5). Gemini stays at 5.

### Changed in 0.26.0

- New `chatgpt.prompt` and `gemini.prompt` (sync and async): send a prompt, get the assistant's
  answer with cited sources, web searches (ChatGPT) and recommended products
  (`POST /api/v1/chatgpt/prompt`, `POST /api/v1/gemini/prompt`). 5 credits per answered prompt at launch.
- Endpoints can now declare a minimum request timeout; these two raise it to 120s when the
  client's `timeout` is shorter. A longer client timeout is always kept.

### Changed in 0.25.0

- New `google.custom_search` (sync and async): Google search in the Custom Search JSON API
  format (`POST /api/v1/google/customsearch`). Snake_case arguments map to the CSE wire names
  (`site_search` -> `siteSearch`, `date_restrict` -> `dateRestrict`, ...). 1 credit.

### Changed in 0.24.1

- Docstring wording only: parameter notes describe what each endpoint returns. No price, parameter or behavior changed.

### Changed in 0.24.0

- **Instagram is cheaper.** Typical costs are now 1-2 credits instead of 8-10:
  `profile`, `user_reels`, `user_tagged` and `music_posts` 1 (`user_reels` /
  `user_tagged` 2 the first time a username is looked up), everything else 2.
  `search_users` / `search_hashtags` with a `cursor` cost 8. Any call can cost
  up to 10 when it needs extra work; `credits_used` is always the exact charge.
- **8 new Instagram methods**, sync and async:
  `user_highlights(*, username=None, user_id=None)`,
  `highlight_stories(highlight_id)`,
  `user_similar(*, username=None, user_id=None)`,
  `post_likers(*, shortcode=None, url=None)`,
  `search_reels(keyword, *, cursor=None)`, `search_music(keyword)`,
  `music_posts(music_id, *, cursor=None)` and `search_locations(keyword)`.
- `user_posts` still returns its existing shape: items under `data.data.items`,
  next page via `data.pagination_token`.

```python
hl = client.instagram.user_highlights(username="natgeo")
stories = client.instagram.highlight_stories("highlight:18149897764550869")
track_reels = client.instagram.music_posts("1747512212697470")
```

### Changed in 0.23.0

- **`client.extract` is now a callable namespace.** `client.extract(url,
  format=..., mode=...)` works exactly as before (same signature, same request
  on the wire, sync and async), and the same object adds the website map,
  crawl and batch operations: `extract.map`, `extract.crawl`,
  `extract.crawl_status`, `extract.cancel_crawl`, `extract.batch`,
  `extract.batch_status`, `extract.cancel_batch`. `crawl` and `batch` take
  `wait=True` to poll until done and return every result. See example 17b.
- **`scavio.verify_webhook(secret, header, body)`** verifies the signed
  completion webhooks crawl and batch jobs send.
- New `ScavioJobTimeoutError` (a `ScavioTimeoutError`) when `wait_timeout`
  elapses; it carries `job_id`.
- **`tiktok.video_transcript(video_id=None, *, url=None, language=None)`**:
  the spoken-word transcript of a TikTok video as timestamped segments and full
  text, 1 credit. Returns `available: false` for videos with no spoken captions.
- 2xx responses other than 200 (a job's 202) are now treated as success.

```python
site = client.extract.map("https://scavio.dev", limit=50)
crawl = client.extract.crawl("https://scavio.dev/docs", max_pages=2, wait=True)
words = client.tiktok.video_transcript("7609177768793787679")
```

### Changed in 0.22.0

- **19 new methods across TikTok, YouTube, Reddit and X, 1 credit each.**
  - `tiktok`: `trending_searches()`, `trending_videos()` (about 6 videos per
    call whatever `count` says), `search_suggestions(keyword)`,
    `music(music_id)`, `music_videos(music_id)` (`count` is ignored upstream,
    about 14 per page), `search_music(keyword)`, `music_chart()` (Top 50 or
    Viral 50, one global chart), `user_similar(sec_user_id)`,
    `user_playlists(sec_user_id)`, `playlist_videos(playlist_id)`,
    `user_live(username)` (an unknown username is a billed 404) and
    `user_region(username)` (an unknown username is an unbilled 404; also
    returns `sec_user_id`). These return TikTok's raw payload: large numeric
    ids can lose precision as JSON numbers, so use `id_str` / `sec_uid`.
  - `youtube`: `community_post(post_id)`, `community_post_comments(post_id)`.
  - `reddit`: `search_comments(query)` (sort `RELEVANCE`, `HOT`, `TOP` or
    `NEW`), `search_subreddits(query)`.
  - `x`: `search_communities(keyword)`, `community(community_id)`,
    `community_tweets(community_id)` (ranking `Relevance` or `Recency`).
- `youtube.transcript` now costs 5 credits (was 8); the docstring says so.

```python
chart = client.tiktok.music_chart(chart="viral", count=10)
region = client.tiktok.user_region("mrbeast")
similar = client.tiktok.user_similar(region["data"]["sec_user_id"])
threads = client.reddit.search_comments("web scraping api", sort="NEW")
posts = client.x.community_tweets("1508567430188126209", ranking="Recency")
```

### Changed in 0.21.1

- README: Mercado Libre docs and landing page links; wording cleanup. No
  behavior changes.

### Changed in 0.21.0

- **New `mercadolibre` namespace, 5 methods.** `search` (keyword or seller in
  Mexico, Brazil, Argentina or Colombia; condition, price, discount, free
  shipping, Full fulfillment, official store and interest-free installment
  filters; relevance or price sort; 2 credits), `product` (buy-box seller,
  variations, star distribution, specs; 2), `reviews` (15 per page with a star
  filter; 1), `questions` (buyer questions with seller answers; 2) and
  `best_sellers` (top 20 in a category, not Brazil; 2). `country` is required
  on `search` and `best_sellers` and is keyword-only. See example 23 above.
- `realtor.search(keywords=...)` docstring: a listing must contain ALL the
  keywords, so each extra keyword narrows the results.

### Changed in 0.20.1

- README: Realtor.com and Rightmove docs links; Rightmove sold prices cover
  England and Wales only, and search pages return 24-25 rows (the
  `rightmove.search(page=...)` docstring now says so). No behavior changes.

### Changed in 0.20.0

- **New `realtor` namespace, 6 methods, 1 credit each.** `search` (for sale,
  pending, for rent or sold by location, radius or agent; price, beds, baths,
  sqft, lot, garage, HOA, year built, property type, recency, listing-text
  keywords and more; up to 200 rows per call), `property` (price and tax
  history, valuations, schools, risk, listing agent), `locations`, `market`,
  `agents` and `agent`.
- **New `rightmove` namespace, 7 methods, 1 credit each.** `locations`,
  `search` (buy or rent by location, place name or branch), `property`, `sold`
  (sale history since 1995 per address plus an area summary), `sold_property`,
  `agents` and `agent`. See example 22 above.

### Changed in 0.19.1

- `trustpilot.category(min_trust_score=...)` docstring corrected: the filter
  is a minimum star rating (3, 4 or 4.5). Trustpilot rounds TrustScore to
  stars, so 4 includes TrustScore 3.8 and up. No code changes.

### Changed in 0.19.0

- **New `trustpilot` namespace, 6 methods, 2 credits each.** `search`
  (businesses by keyword, up to 100 per page), `business` (full profile by
  domain or Trustpilot URL), `reviews` (stars, language, date range, sort,
  verified-only, with-replies, topics and text filters; up to 200 per filter
  combination), `categories` (the tree or a name lookup), `category` (ranked
  businesses with sort, minimum star rating and claimed-only) and `review` (one
  review by id). See example 21 above.

### Changed in 0.18.1

- Documentation links only; no code changes. The client already identifies
  itself on every call with `User-Agent: scavio-python/<version>` and
  `X-Client-Source: scavio-python`.

### Changed in 0.18.0

- **New `costco` namespace, 13 methods.** `search`, `category`, `categories`,
  `product` (up to 20 ids per call), `prices` (online vs in-warehouse price at up
  to 10 warehouses), `availability` (in-warehouse stock status), `reviews`,
  `warehouses`, `gas`, `coupons` (the member coupon book), `deals`
  (new, while_supplies_last, treasure_hunt, member_favorites, online_only,
  on_sale), `clearance` (price-code markdown finder) and `autocomplete`. See
  example 20 above.

### Changed in 0.17.0

- **Walmart store targeting.** `walmart.stores(zipcode, domain=...)` is new: it
  returns the Walmart stores near a US ZIP (walmart.com) or a Canadian postal
  code (`domain="ca"`, walmart.ca), nearest first, each with its `store_id`.
  Pass that `store_id` together with `delivery_zip` to `walmart.search()` or
  `walmart.product()` on the same domain to get that store's assortment and
  availability; `data.location` echoes the store used. Store-targeted calls
  cost 2 credits and take 10-60 seconds, so give them a generous timeout.
  `walmart.product()` also accepts `domain="ca"`, together with a store pair.

  ```python
  stores = client.walmart.stores("50036")
  store_id = stores["data"]["stores"][0]["store_id"]  # "1389", Boone Supercenter
  milk = client.walmart.search("whole milk", delivery_zip="50036", store_id=store_id)
  print(milk["data"]["location"])  # {"city": "Boone", "state": "IA", "store_id": "1389", ...}
  ```
- `delivery_zip` and `store_id` are no longer retired; `device` is now the only
  retired Walmart parameter.

### Changed in 0.16.0

- **`max_requests_per_second` now accepts up to 50** (it was capped at 10),
  matching the raised per-plan request limits -- the top plan allows 50, so
  the old ceiling rejected a value the plan entitled you to. The default is
  still 1, and the bound now lives in one place
  (`scavio._ratelimit.MAX_REQUESTS_PER_SECOND`) shared by the sync and async
  clients.

### Changed in 0.15.0

- **21 new namespaces with 85 endpoints**: Threads, Kuaishou, eBay, Target,
  Home Depot, Zillow, Redfin, Booking.com, Tripadvisor, Airbnb, Yelp, Indeed,
  Glassdoor, Apple App Store, Google Play, SEC EDGAR, Companies House, G2,
  Capterra, Google Ads Transparency and the Meta Ad Library. With the Walmart
  rebuild and `extract` below, that is 93 endpoints in this batch and 195 in the
  SDK. Every method is typed and documented inline, on both the sync and async
  clients.
- **`client.extract(url, format=..., mode=...)` is new, and is a top-level
  method, not a namespace.** Reading an arbitrary URL is a core capability
  rather than a platform, so it is `client.extract(...)`, never
  `client.extract.extract(...)`.
- **Walmart grew from 2 endpoints to 7** (`reviews`, `category`, `offers`,
  `seller`, `seller_products` are new) and `search`/`product` changed shape.
  `device`, `delivery_zip` and `store_id` are retired: the API answers 200 with
  a top-level `warnings` array if you send them through `**extra`. `domain`
  (`com` | `ca` | `com.mx`) is new on `search` and `category`, and it is the
  price-bearing parameter. `page` supersedes `start_page`, which stays as a
  deprecated alias.
- **Walmart `min_price` / `max_price` widened from `int` to `float`.** The
  backend was always `z.number()`, so `19.99` was always accepted; the old
  annotation was simply wrong. No runtime behaviour changed.
- **Four surfaces are body-priced and their docstrings say so** instead of
  quoting a flat price: Walmart (`com.mx` costs 2), Threads (4 credits when
  addressed by `username` instead of `user_id`), Kuaishou (1, 2, 10 or 40 per
  endpoint) and `extract` (`mode="ultra"` costs 2).
- Some caveats worth knowing before you write a loop: eBay `sold=True` returns
  `total_results: null`; Meta Ad Library pages are 30 ads then 10, and the
  cursor ignores every other filter; Capterra `search` does not paginate at all;
  Apple App Store `search` has no pagination either (raise `limit`, up to 200);
  Airbnb prices exist only on `search`, never on `listing`.

### Changed in 0.14.0

- `reddit.post()` now takes `post_id` as well as `url` -- pass either one. `url`
  stays the first positional argument, so existing calls are unaffected.
  The response is a flat post object and carries no comments; use
  `reddit.post_comments()` for those.
- `youtube.shorts(sort_by=...)` is now typed as
  `relevance | date | view_count | rating` instead of a free-form string.
- `youtube.search()` lost its `location` flag. It was never part of the backend
  schema, so it was silently dropped rather than filtering anything.

### Amazon changed in 0.12.0 (breaking)

The Amazon API now returns a normalized shape instead of the previous raw
payload.

- `search` returns `{query, page, total_results, total_results_text, count, products[], filters[], related_searches[]}`.
  Each product is `{asin, title, url, image, price, currency, rating, reviews_count, is_sponsored, position, badge, sales_volume, delivery{is_free, date, fastest_date}}`.
- `product` returns flat fields: `price`, `list_price`, `currency`, `rating`, `reviews_count`, `features`, `images`, `videos`, `variants`, `specifications`, `best_sellers_rank`, `shipping`, and more. The old `buybox[]` array no longer exists -- use `offers` for per-seller pricing.
- `offers` is new: every seller for one ASIN, with `price`, `condition`, `seller_name`, `is_buy_box_winner`, `is_fulfilled_by_amazon`, and delivery windows.
- `country` (ISO 3166-1 alpha-2: `us`, `gb`, `de`) is the marketplace selector and replaces `domain`. `page` replaces `start_page`. The old names still work as deprecated aliases.
- Nine parameters were removed: `language`, `currency`, `device`, `sort_by`, `pages`, `category_id`, `merchant_id`, `zip_code`, `autoselect_variant`. `sort_by` in particular was verified to be ignored by the marketplace, so result sorting is not available at any layer. Sending one of them anyway (via `**extra`) still returns 200, with a top-level `warnings` array explaining what was ignored.
- `options` still returns `domains` and `countries`; `languages` and `currencies` are now always empty, because neither is a request parameter any more.

## Links

- [Website](https://scavio.dev?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
- [Documentation](https://docs.scavio.dev)
- [Dashboard & API Keys](https://dashboard.scavio.dev/sign-up?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
- [API Reference](https://docs.scavio.dev/api-reference)
- [Compare Scavio vs alternatives](https://scavio.dev/compare?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)

## License

MIT


## About Scavio

[Scavio](https://scavio.dev?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) is a unified [search API](https://scavio.dev/docs/search-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) built for AI agents — one API key, structured JSON. A real-time [Tavily alternative](https://scavio.dev/alternatives/tavily?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) and [SerpAPI alternative](https://scavio.dev/alternatives/serpapi?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) with data from:

- [Google Search API](https://scavio.dev/google-search-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — SERP results, news, images, maps, and knowledge graph
- [Amazon Product API](https://scavio.dev/amazon-product-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) and [Walmart Product API](https://scavio.dev/walmart-product-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — product search and details
- [YouTube API](https://scavio.dev/youtube-transcript-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [TikTok API](https://scavio.dev/tiktok-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), and [Instagram API](https://scavio.dev/instagram-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — video and social media data
- [TikTok Shop API](https://scavio.dev/docs/tiktok-shop-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — product search, detail, reviews, categories, and shop catalogs
- [Reddit API](https://scavio.dev/reddit-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — posts, comments, subreddits, and trending
- [X API](https://scavio.dev/docs/x-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) and [LinkedIn API](https://scavio.dev/docs/linkedin-person?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — tweets, profiles, companies, and jobs

For a detailed head-to-head breakdown, see [Tavily vs Scavio](https://scavio.dev/compare/tavily/vs-scavio?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

Get a free [API key](https://dashboard.scavio.dev/sign-up?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) and explore the [documentation](https://scavio.dev/docs/introduction?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).
