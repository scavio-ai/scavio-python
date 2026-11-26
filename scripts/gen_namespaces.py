#!/usr/bin/env python3
"""Generate the sync and async namespace classes from ``scavio/_spec.py``.

The generated modules (``scavio/_namespaces_sync.py`` and
``scavio/_namespaces_async.py``) contain one class per provider, each with fully
typed, individually documented methods. Because both files are emitted from the
same spec by the same template, the sync and async surfaces are guaranteed to
stay in lock-step (a property additionally enforced by tests/test_parity.py).

Usage:
    python scripts/gen_namespaces.py        # rewrite both generated modules
    python scripts/gen_namespaces.py --check # fail if they are out of date
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import textwrap
from pathlib import Path

_PKG_ROOT = Path(__file__).resolve().parent.parent


def _load_spec():
    """Import scavio/_spec.py in isolation.

    Loading the module by path (rather than ``import scavio._spec``) avoids
    triggering the package ``__init__``, which imports the very namespace
    modules this script generates.
    """
    spec_path = _PKG_ROOT / "scavio" / "_spec.py"
    module_spec = importlib.util.spec_from_file_location("_scavio_spec", spec_path)
    assert module_spec and module_spec.loader
    module = importlib.util.module_from_spec(module_spec)
    # Register before exec so dataclass processing can resolve cls.__module__.
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    return module


_spec = _load_spec()
NAMESPACES = _spec.NAMESPACES
Endpoint = _spec.Endpoint
endpoints_for = _spec.endpoints_for

# Human-facing class name and one-line description per namespace.
_NS_META = {
    "google": ("Google", "Google endpoints (SERP, Maps, Shopping, Flights, Hotels, News, Trends)."),
    "amazon": ("Amazon", "Amazon product search, product detail, and seller offer endpoints."),
    "walmart": ("Walmart", "Walmart product search and lookup endpoints."),
    "youtube": ("YouTube", "YouTube search, video, transcript, channel, comment, and streams endpoints."),
    "reddit": ("Reddit", "Reddit search, post, comment, subreddit, user, and trending endpoints."),
    "x": ("X", "X search, tweet, and user endpoints."),
    "tiktok": ("TikTok", "TikTok profile, video, transcript, hashtag, and search endpoints."),
    "instagram": ("Instagram", "Instagram profile, media, and search endpoints."),
    "linkedin": ("LinkedIn", "LinkedIn person, company, job, post, and search endpoints."),
    "tiktok_shop": (
        "TikTokShop",
        "TikTok Shop search, product, review, category, shop, and URL-resolution endpoints.",
    ),
    "threads": ("Threads", "Threads profile, post, comment, and people-search endpoints."),
    "kuaishou": (
        "Kuaishou",
        "Kuaishou (China) profile, video, comment, search, tag, and trending endpoints.",
    ),
    "ebay": ("Ebay", "eBay live and sold listing search, listing detail, and seller endpoints."),
    "target": ("Target", "Target search, category, product, and review endpoints."),
    "home_depot": (
        "HomeDepot",
        "Home Depot search, product, review, store, availability and shipping endpoints "
        "(homedepot.com by default); country='ca' reads Home Depot Canada (homedepot.ca, CAD, "
        "prices and exact units per store; no shipping), which also has category, categories, "
        "stock, store and suggestions endpoints.",
    ),
    "zillow": ("Zillow", "Zillow listing search, property detail, and agent-review endpoints."),
    "booking": ("Booking", "Booking.com property search, hotel detail, and review endpoints."),
    "tripadvisor": (
        "Tripadvisor",
        "Tripadvisor location lookup, listing search, location detail, and review endpoints.",
    ),
    "indeed": ("Indeed", "Indeed job search, job detail, company, and company-review endpoints."),
    "airbnb": ("Airbnb", "Airbnb stay search, listing detail, and review endpoints."),
    "glassdoor": (
        "Glassdoor",
        "Glassdoor company lookup, employer profile, review, and salary endpoints.",
    ),
    "yelp": ("Yelp", "Yelp business search, business detail, and review endpoints."),
    "app_store": ("AppStore", "Apple App Store search, app detail, and review endpoints."),
    "google_play": ("GooglePlay", "Google Play search, app detail, and review endpoints."),
    "sec": (
        "SEC",
        "SEC EDGAR company lookup, filer profile, filings, XBRL facts, and full-text search.",
    ),
    "redfin": ("Redfin", "Redfin listing search, property detail, and market-stats endpoints."),
    "companies_house": (
        "CompaniesHouse",
        "UK Companies House register search, company, officer, and filing-history endpoints.",
    ),
    "g2": ("G2", "G2 software search, product profile, and review endpoints."),
    "capterra": ("Capterra", "Capterra software search, product profile, and review endpoints."),
    "google_ads": (
        "GoogleAds",
        "Google Ads Transparency advertiser lookup, ad search, and creative endpoints.",
    ),
    "meta_ads": (
        "MetaAds",
        "Meta Ad Library keyword search, advertiser ads, and single-ad endpoints.",
    ),
    "costco": (
        "Costco",
        "Costco search, product, warehouse price, stock, gas, coupon, deal, and clearance endpoints.",
    ),
    "trustpilot": (
        "Trustpilot",
        "Trustpilot business search, profile, review, and category endpoints.",
    ),
    "realtor": (
        "Realtor",
        "Realtor.com listing search, property, location, market, and agent endpoints.",
    ),
    "rightmove": (
        "Rightmove",
        "Rightmove UK property search, listing, sold price, and agent endpoints.",
    ),
    "mercadolibre": (
        "MercadoLibre",
        "Mercado Libre listing search, product, review, question, and best-seller endpoints.",
    ),
    "chatgpt": (
        "ChatGPT",
        "ChatGPT answers with cited sources, web searches and recommended products.",
    ),
    "gemini": (
        "Gemini",
        "Google Gemini answers with cited sources and recommended products.",
    ),
    "decathlon": (
        "Decathlon",
        "Decathlon sporting goods search and product detail across 7 country domains.",
    ),
    "specs": (
        "Specs",
        "Spec's search, product detail with every store's price, and store locator endpoints.",
    ),
    "lowes": (
        "Lowes",
        "Lowe's store-level search, product detail, store locator, and review endpoints.",
    ),
    "sams_club": (
        "SamsClub",
        "Sam's Club search, club-level product detail, club locator, Instant Savings, category, and review endpoints.",
    ),
    "canadian_tire": (
        "CanadianTire",
        "Canadian Tire store-level search, product, store locator, availability, clearance, and deal endpoints.",
    ),
    "dollar_general": (
        "DollarGeneral",
        "Dollar General store-level search, product, store locator with unit counts, deal, and coupon endpoints.",
    ),
    "sephora": (
        "Sephora",
        "Sephora search, category, and product detail endpoints with per-shade stock and review "
        "sentiment (sephora.com by default); country='ca' reads Sephora Canada (sephora.com/ca, "
        "CAD), which also has brand, brands, suggestions, offers, stores and store endpoints.",
    ),
    "ulta": (
        "Ulta",
        "Ulta Beauty search, category, product detail, and nearby-store availability endpoints.",
    ),
    "aldi": (
        "Aldi",
        "ALDI store-level search, product detail, and store locator endpoints (in-store, pickup or delivery prices).",
    ),
    "micro_center": (
        "MicroCenter",
        "Micro Center store-level search, product detail with open-box units, and store list endpoints.",
    ),
    "walgreens": (
        "Walgreens",
        "Walgreens search, product detail, store locator, and multi-store stock endpoints.",
    ),
    "cvs": (
        "Cvs",
        "CVS search, product detail, and per-store stock endpoints.",
    ),
    "whole_foods": (
        "WholeFoods",
        "Whole Foods Market store-level search, category, deal, product, store, and sales flyer endpoints.",
    ),
    "harbor_freight": (
        "HarborFreight",
        "Harbor Freight search, clearance, product, batch price, store locator, store stock, and review endpoints.",
    ),
    "petsmart": (
        "Petsmart",
        "PetSmart search, product detail, store locator with unit counts, store stock, and deal endpoints.",
    ),
    "petco": (
        "Petco",
        "Petco search, category, product detail, store locator, and store inventory endpoints.",
    ),
    "iherb": (
        "Iherb",
        "iHerb search, product detail, batch price, and review summary endpoints (online only).",
    ),
    "chewy": (
        "Chewy",
        "Chewy search and product detail endpoints with one-time and Autoship prices.",
    ),
    "menards": (
        "Menards",
        "Menards product detail with rebates and per-store stock, and store locator endpoints.",
    ),
    "nordstrom": (
        "Nordstrom",
        "Nordstrom search, category, brand, product, reviews, pickup availability, store locator, and autocomplete endpoints.",
    ),
    "nordstrom_rack": (
        "NordstromRack",
        "Nordstrom Rack search, category (clearance, flash events), brand, product, reviews, pickup availability, store locator, and autocomplete endpoints.",
    ),
    "best_buy": (
        "BestBuy",
        "Best Buy search, product (open-box offers), reviews, category, Deal of the Day, "
        "store locator, store pickup availability, autocomplete, and batch price endpoints "
        "(bestbuy.com by default); country='ca' reads Best Buy Canada (bestbuy.ca, CAD, exact "
        "units per store, EHF by province), which also has a questions endpoint.",
    ),
    "tcgplayer": (
        "Tcgplayer",
        "TCGplayer card and sealed product search, product (per-SKU market price), live listings, "
        "price history, recent sales, games, sets, set price guide, autocomplete, trending, and "
        "seller endpoints.",
    ),
    "vinted": (
        "Vinted",
        "Vinted second-hand listing search, product, seller profile, seller listings, seller "
        "feedback, brands, autocomplete, filters, and category endpoints across 27 country sites.",
    ),
    "macys": (
        "Macys",
        "Macy's search, product (batch of 10), reviews, category, brand, deals (clearance, Last "
        "Act, Black Friday), store locator, store pickup availability, and autocomplete endpoints.",
    ),
    "saks": (
        "Saks",
        "Saks Fifth Avenue search, product, category, designer page, sale and new-arrival "
        "listings, store locator, store pickup availability, suggestions, and designer index "
        "endpoints.",
    ),
    "kohls": (
        "Kohls",
        "Kohl's search, product, category, brand page, clearance / sale / Kohl's Cash / Sephora "
        "listings, store locator, store pickup stock, suggestions, and coupon code endpoints.",
    ),
    "jcpenney": (
        "Jcpenney",
        "JCPenney search, product (batch of 20), category, brand, clearance / sale / Black Friday "
        "/ BOGO deal listings, store locator, store unit counts, suggestions, coupon code, "
        "review text and Q&A endpoints.",
    ),
    "dicks": (
        "Dicks",
        "Dick's Sporting Goods search, per-SKU product detail, batch product summary, newest "
        "reviews, category, brand, clearance / sale / weekly deal listings, store unit counts "
        "(DICK'S, Golf Galaxy, Public Lands) and suggestion endpoints.",
    ),
    "footlocker": (
        "Footlocker",
        "Foot Locker search, product detail with per-size availability, category, brand, sale / "
        "exclusives / promo-eligible deal listings, release calendar, store locator, store "
        "availability, review and Q&A endpoints across 13 storefronts.",
    ),
    "fanatics": (
        "Fanatics",
        "Fanatics merchandise search, product detail with per-size stock levels and "
        "personalization, team / player / league / brand listings, sale / clearance / under-25 "
        "deals and review endpoints across 8 storefronts and 4 US league stores.",
    ),
    "carrefour": (
        "Carrefour",
        "Carrefour grocery search with national or store-level prices, product detail with "
        "Nutri-Score, ingredients and nutrition, reviews, category and promotion listings, "
        "suggestions, store locator, store availability and store detail with fuel prices "
        "(carrefour.fr; search and product also on Argentina, Romania and Belgium).",
    ),
    "allegro": (
        "Allegro",
        "Allegro marketplace search, offer detail with the 30-day lowest price and auction "
        "state, catalogue product with the first 20 reviews, every seller's offer for one "
        "product, seller offers and seller feedback, and category listings (allegro.pl, plus "
        "allegro.cz, allegro.sk and allegro.hu).",
    ),
    "olx": (
        "Olx",
        "OLX Europe classifieds search, ad detail, seller and seller ads, category filters, "
        "category tree, location and search suggestions, and similar ads (olx.pl, plus olx.ro, "
        "olx.pt, olx.bg, olx.ua, olx.kz and olx.uz).",
    ),
    "company": (
        "Company",
        "Company enrichment: a company's published emails, phone numbers, social profiles, "
        "contact page and owner from its website or a Google Maps place_id.",
    ),
    "heb": (
        "Heb",
        "HEB grocery search, product detail, and store locator endpoints, store-targetable.",
    ),
    "kroger": (
        "Kroger",
        "Kroger, QFC and Fred Meyer grocery search, product detail, store-level prices, store "
        "locator, category, weekly digital deals, digital coupons and search suggestion endpoints.",
    ),
    "publix": (
        "Publix",
        "Publix grocery search, product and nutrition, category, category tree, weekly ad, "
        "Extra Savings, digital coupons, savings search, deli and bakery order-ahead menu, store "
        "locator and search suggestion endpoints, store-scoped.",
    ),
    "ikea": (
        "Ikea",
        "IKEA search, product, reviews, category, category tree, deal lists, search suggestion, "
        "store locator, stock by store, bulk item lookup, prices by country and As-is offer "
        "endpoints, across 55 markets.",
    ),
    "wayfair": (
        "Wayfair",
        "Wayfair search, product, category and sale event endpoints for wayfair.com, "
        "wayfair.ca, wayfair.co.uk and wayfair.ie, plus the AllModern, Birch Lane, Joss & Main "
        "and Perigold sites.",
    ),
    "ashley": (
        "Ashley",
        "Ashley Furniture search, product, category, deal event, store locator and store "
        "endpoints for ashleyfurniture.com, plus search and product on Ashley's licensed "
        "storefronts in Canada, Mexico, the Philippines, Saudi Arabia and Turkey.",
    ),
    "maisonsdumonde": (
        "MaisonsDuMonde",
        "Maisons du Monde search, product, category, deals, reviews, store finder, store, "
        "store stock and marketplace seller endpoints for France, Belgium (French or Dutch), "
        "Luxembourg, the Netherlands, Germany, Spain, Italy, Portugal and Switzerland (French, "
        "German or Italian).",
    ),
    "trendyol": (
        "Trendyol",
        "Trendyol search, product (buy box and every other seller), category, brand, reviews, "
        "questions, seller, deals, coupons, rankings, suggestions and delivery endpoints for "
        "the Turkish storefront and Trendyol's international storefronts (35 markets).",
    ),
    "nintendo": (
        "Nintendo",
        "Nintendo eShop search, product, prices (one game's price, sale price and sale end in "
        "each eShop country), deals, releases and DLC endpoints for 46 countries across the "
        "Americas, Europe, Oceania, South Africa, Japan, Korea, Hong Kong and Taiwan.",
    ),
    "hm": (
        "Hm",
        "H&M search, product (prices, member price, colours, online stock by size, rating and "
        "the latest reviews), stock, stores, category, deals, new arrivals, suggestions and "
        "production endpoints for 47 countries across Europe, the Americas, the Middle East, "
        "Asia and Australia.",
    ),
    "zara": (
        "Zara",
        "Zara search, product, materials, online stock, stores, store stock, categories, "
        "category, deals, new arrivals, prices by country and suggestions endpoints for 102 "
        "storefronts across Europe, the Americas, the Middle East, Africa, Asia and Oceania.",
    ),
    "asos": (
        "Asos",
        "ASOS search, product, online stock by size, reviews, suggestions, category, categories, "
        "brands, deals, new arrivals and markets endpoints for 235 countries (13 ASOS stores, "
        "245 country-currency combinations).",
    ),
    "mercari": (
        "Mercari",
        "Mercari search (on sale and sold), item, category, categories, brands, brand, deals and "
        "trending endpoints for Mercari US and Mercari Japan, plus Mercari Japan seller, seller "
        "reviews and Mercari Shops shop endpoints.",
    ),
    "bolcom": (
        "Bolcom",
        "bol.com search, product (by id, link or EAN), offers (the 10 lowest-priced), seller, "
        "seller products, category, brand, deals and campaign endpoints for the bol.com "
        "storefronts nl-nl, be-nl and be-fr (the Netherlands and Belgium, EUR).",
    ),
    "uniqlo": (
        "Uniqlo",
        "Uniqlo search, product, online stock, store stock, stores, reviews, suggestions, "
        "category, deals, new arrivals, categories and prices by country endpoints: every "
        "endpoint on us, jp and kr, search + product on tw, hk and cn, product + prices on 35 "
        "more storefronts across Europe, Asia-Pacific and Canada.",
    ),
    "depop": (
        "Depop",
        "Depop search, product, category, brand, explore and suggestions endpoints for the "
        "buyer markets us, gb, au, ie, ca, nz, de, fr and it, plus global shop, shop products, "
        "shop sold, shop reviews, shops search, categories and brands endpoints and US similar "
        "listings.",
    ),
    "poshmark": (
        "Poshmark",
        "Poshmark search, sold, category, brand, brands, suggestions, parties, party listings "
        "and similar endpoints for poshmark.com (us) and poshmark.ca (ca), plus global listing, "
        "closet, closet listings, Love Notes, closets search and category tree endpoints.",
    ),
    "thredup": (
        "Thredup",
        "thredUP search, sold, product, category, brand, deals, rescue boxes, categories, brands, "
        "suggestions, trending and similar endpoints for thredUP's US store (thredup.com, USD).",
    ),
    "fashionnova": (
        "Fashionnova",
        "Fashion Nova search, product, collection, categories, suggestions, reviews and similar "
        "endpoints across Fashion Nova's 104 country storefronts (local currency, en or es).",
    ),
    "argos": (
        "Argos",
        "Argos search, product, store stock, stores, reviews, questions, categories, category, "
        "deals and suggestions endpoints for argos.co.uk (UK, GBP).",
    ),
    "mediaexpert": (
        "MediaExpert",
        "Media Expert search, product, store stock, stores, reviews, category, categories, brands, "
        "brand, promotions, outlet, seller and suggestions endpoints for mediaexpert.pl (Poland, PLN).",
    ),
    "action": (
        "Action",
        "Action (action.com, the European non-food discount store) search, product, products, "
        "category, categories, brand, brands, new arrivals, weekly deals, collection, suggestions, "
        "stores, store, reviews and webshop endpoints for 19 storefronts in 16 countries.",
    ),
    "hema": (
        "Hema",
        "HEMA (hema.com, the Dutch variety store) search, product, category, categories, new "
        "arrivals, sale, offers, campaign, suggestions, store stock, stores, store and reviews "
        "endpoints for the nl, be, fr and de webshops (stores also lu and at).",
    ),
    "autozone": (
        "Autozone",
        "AutoZone (autozone.com, the US auto parts retailer) search, product, category, brand, "
        "vehicles, reviews, stores, store, categories, clearance, rebates and store stock "
        "endpoints (also autozone.com.br and autozone.com.mx).",
    ),
    "instacart": (
        "Instacart",
        "Instacart (instacart.com, the US and Canada grocery delivery and pickup marketplace) "
        "retailers, search, cross-store search, product, price compare, categories, category, "
        "deals, stores, suggestions and reviews endpoints (also instacart.ca).",
    ),
    "oreilly": (
        "Oreilly",
        "O'Reilly Auto Parts (oreillyauto.com, the US auto parts retailer) search, "
        "cross-reference, product, vehicles, compatibility, category, categories, brand, store "
        "stock, stores, store, suggestions, rebates and deals endpoints (store directory also "
        "for Mexico).",
    ),
    "acehardware": (
        "Acehardware",
        "Ace Hardware (acehardware.com, the US hardware cooperative) search, product (priced "
        "for an Ace store), store stock (exact units at up to 25 stores or a store and its 25 "
        "nearest), store, stores, category, categories, brand, deals, weekly ad and paint "
        "colors endpoints.",
    ),
    "tractorsupply": (
        "Tractorsupply",
        "Tractor Supply (tractorsupply.com, the US rural lifestyle retailer) search, product "
        "(priced for one store or ZIP), store prices (one item at up to 25 stores), store stock "
        "(exact units and in-transit stock at up to 25 stores), fulfillment, stores, store, "
        "category, categories, brand, deals and promotions endpoints.",
    ),
    "michaels": (
        "Michaels",
        "Michaels (michaels.com, the US and Canada arts and crafts retailer) search, product, "
        "store stock (exact units at the stores near a ZIP or postal code), store inventory (up "
        "to 30 SKUs at one store), stores, store, category, categories, brand, deals and "
        "suggestions endpoints.",
    ),
    "nike": (
        "Nike",
        "Nike (nike.com, including Jordan Brand) search, product (every size with its GTIN), "
        "category, brand (Jordan, ACG, SB), deals, releases (the launch calendar with per-size "
        "levels), release and reviews endpoints, on 62 storefronts.",
    ),
    "staples": (
        "Staples",
        "Staples (staples.com, the US office supply retailer; Staples Canada at staples.ca) "
        "search, product (price per unit, page yield, promotions), category, categories, deals, "
        "coupons, store-stock (units at the stores near a ZIP), stores, store, reviews, "
        "questions and trending endpoints.",
    ),
    "dollartree": (
        "DollarTree",
        "Dollar Tree (dollartree.com, the US and Canada discount variety store chain) search, "
        "product (unit price, case price, case pack, minimum quantity), category, categories, "
        "brand, deals (sale, clearance, New Arrivals, More Choices), store-stock (units at a "
        "store and its nearby stores), stores, store and reviews endpoints.",
    ),
    "discounttire": (
        "DiscountTire",
        "Discount Tire (discounttire.com, the US tire and wheel retailer, America's Tire in "
        "parts of CA, PA, NJ and NY) search (tires by size), vehicle (year, make, model, trim, "
        "size option, fitment), vehicle-tires, product, model, store-stock (exact units at the "
        "stores near a ZIP), stores, store, reviews, store-reviews, wheels, browse, categories, "
        "suggestions and appointments (read only) endpoints; prices are per store.",
    ),
    "vevor": (
        "Vevor",
        "VEVOR (vevor.com, the tools and equipment seller with storefronts in 13 countries) "
        "search, product, shipping (fee and delivery date by US state or Canadian province), "
        "reviews, questions, suggestions, categories, category, collections, deals and prices "
        "(the same SKU on all 13 storefronts) endpoints; prices are per storefront.",
    ),
    "nellis": (
        "Nellis",
        "Nellis Auction (nellisauction.com, the liquidation auction marketplace with pickup "
        "warehouses in Las Vegas, Phoenix, Houston, Philadelphia, Denver and Dallas) search "
        "(open auctions), item (open, closed or sold, with the bid history and a sold item's "
        "final price), locations and categories endpoints; per shopping location.",
    ),
    "dermstore": (
        "Dermstore",
        "Dermstore (dermstore.com, the US skincare and beauty retailer, shipping to the US and "
        "Canada) search, list (any list page by path), product (variants, UPC, offer banner, the 10 "
        "latest reviews), suggestions, offers (with end times), brands and categories endpoints; "
        "us or ca (Dermstore's own CAD prices).",
    ),
    "offerup": (
        "Offerup",
        "OfferUp (offerup.com, the US local marketplace for buying and selling used items, cars "
        "and trucks) search (around a US ZIP), listing (condition, posted date, vehicle details, "
        "no VIN), category, categories and seller (public profile numbers, the first 20 "
        "listings) endpoints; US only, asking prices in USD.",
    ),
    "sportchek": (
        "Sportchek",
        "SportChek (sportchek.ca, Canada's sporting goods retailer, a Canadian Tire Corporation "
        "banner) search, list (category and deals pages by path), product (variants with their "
        "own price, was price and sale end date, units at the assigned store and online), "
        "reviews, suggestions, store, brands and categories endpoints; English only, prices in "
        "CAD, 1 credit each.",
    ),
    "marks": (
        "Marks",
        "Mark's (marks.com, the Canadian workwear, casual clothing and footwear retailer, a "
        "Canadian Tire Corporation banner; L'Equipeur in French) search, list (category and "
        "deals pages by path), product (variants with their own price, was price and sale end "
        "date, units at the assigned store and online), questions, suggestions, store, brands "
        "and categories endpoints; language en or fr (L'Equipeur) on search, list, product, "
        "brands and categories, prices in CAD, 1 credit each.",
    ),
    "rona": (
        "Rona",
        "RONA (rona.ca, the Canadian home improvement retailer: RONA+ and RONA stores) search, "
        "product, prices (up to 60 articles at one store), category, categories, stores, store, "
        "stock (stores near a store with units) and deals endpoints; Canada only, prices in "
        "CAD, language en or fr.",
    ),
    "pcexpress": (
        "Pcexpress",
        "PC Express (Loblaw's online grocery for Real Canadian Superstore, No Frills, Loblaws, "
        "Zehrs, Fortinos, Valu-mart, Your Independent Grocer, Wholesale Club, Provigo and Maxi) "
        "search, category, collection, product, stores, store and suggestions endpoints; Canada "
        "only, prices in CAD at each banner's default store, banner (10) and language en or fr.",
    ),
    "spacenk": (
        "Spacenk",
        "Space NK (spacenk.com, the London-based luxury beauty retailer) search, category, "
        "brand, brands, product, reviews, suggestions, stores (UK) and offers endpoints; markets "
        "uk, ie, nl, au, each in its own currency; 1 credit each (a full listing up to 5)."
    ),
    "lookfantastic": (
        "Lookfantastic",
        "Lookfantastic (lookfantastic.com, THG's beauty retailer with 10 country sites) search, "
        "list, product, suggestions, offers, brands and categories endpoints; market (10 sites) "
        "and currency on every method, 1 credit each."
    ),
    "cultbeauty": (
        "Cultbeauty",
        "Cult Beauty (cultbeauty.co.uk, THG's beauty retailer) search, list, product, "
        "suggestions, offers, brands and categories endpoints; market gb or intl and currency "
        "(12) on every method, 1 credit each."
    ),
    "yesstyle": (
        "Yesstyle",
        "YesStyle (yesstyle.com, the Hong Kong-based online store for Asian beauty and fashion) "
        "search, category, brand, brands, deals, product, reviews, suggestions and markets "
        "endpoints; prices set per shipping country (39 countries); listings and product 2 "
        "credits, product with variants 3, the rest 1."
    ),
    "notino": (
        "Notino",
        "Notino (notino.com, the Brno-based online perfume and cosmetics store) search, product, "
        "reviews, category, brand, promo, brands, suggestions, stores and store endpoints; 27 "
        "storefronts in their own language and currency; 1 credit (gb 2), a paged, sorted or "
        "filtered list 3 (gb 4)."
    ),
    "douglas": (
        "Douglas",
        "Douglas (douglas.de, the Dusseldorf-based beauty retailer) search, category, brand, "
        "deals, product, stores, store, review_summary, suggestions and brands endpoints; 15 "
        "storefronts in 13 countries; 1 credit each (2 on it)."
    ),
    "boots": (
        "Boots",
        "Boots (boots.com, the UK health and beauty retailer, and boots.ie) product, "
        "store_stock, stores and store endpoints; markets uk and ie; 1 credit each (2 when the "
        "answer comes on a second attempt). No search endpoint: start from a product link."
    ),
    "rockauto": (
        "Rockauto",
        "RockAuto (rockauto.com, the online auto parts catalog) vehicles, categories, parts, "
        "search, brand, brands, part, suggestions, resolve, tools and promotions endpoints; the "
        "US catalog in 15 display currencies, language en, es, fr or de; 1 credit each."
    ),
    "carscom": (
        "Carscom",
        "Cars.com (cars.com, the US car marketplace) search, listing, dealer, dealer_inventory, "
        "dealer_reviews, model_reviews, dealers and research endpoints; US only, prices in USD, "
        "1 credit each."
    ),
    "autotrader": (
        "Autotrader",
        "Autotrader (autotrader.com, the US car marketplace) search, listing, dealers, dealer "
        "and makes endpoints; US only, prices in USD, KBB price ranges as given, 2 credits each."
    ),
    "cargurus": (
        "Cargurus",
        "CarGurus (cargurus.com, the car marketplace in the US, Canada and the UK) search, "
        "dealer, dealers, price_trends, research, expert_reviews, makes and models endpoints; "
        "markets us, us-es, ca, ca-fr, uk; 1 credit each."
    ),
    "carmax": (
        "Carmax",
        "CarMax (carmax.com, the US used-car retailer) search, listing, photos, stores, store, "
        "store_inventory, reviews, review_summary, suggestions, makes, models and car_value "
        "endpoints; US only, prices in USD, 1 credit each."
    ),
    "carvana": (
        "Carvana",
        "Carvana (the US online used-car retailer) search, vehicle, model_guide, trims, make and "
        "makes endpoints; US only, prices in USD, Carvana's own city pages for the location (no "
        "ZIP targeting), 1 credit each."
    ),
    "bringatrailer": (
        "Bringatrailer",
        "Bring a Trailer (bringatrailer.com, the online collector-car auction site) results, "
        "price_history, listing, live, make, model, location and suggestions endpoints; one "
        "site, each lot in its own currency, 1 credit each."
    ),
    "rentcom": (
        "Rentcom",
        "Rent.com (rent.com) and Apartment Guide (apartmentguide.com, same inventory; site rent "
        "or apartmentguide) search, listing, building, rent_trends, suggestions and cities "
        "endpoints; US rentals, rents in USD, 1 credit each."
    ),
    "trulia": (
        "Trulia",
        "Trulia (trulia.com, Zillow Group's home and neighborhood site) neighborhood, search, "
        "property, school and suggestions endpoints; US only, prices in USD, language en or es; "
        "1 credit each."
    ),
    "streeteasy": (
        "Streeteasy",
        "StreetEasy (streeteasy.com, Zillow Group's New York City real estate site) search, "
        "listing, building, buildings and market endpoints; NYC and North NJ (market data NYC "
        "only), prices in USD, 1 credit each."
    ),
    "rentcafe": (
        "Rentcafe",
        "RentCafe (rentcafe.com, Yardi's US and Canada rental listing site) search, property, "
        "floorplan_units, reviews, suggestions and rent_trends endpoints; markets us and ca "
        "(English or French), rents in USD or CAD, 1 credit each."
    ),
    "vrbo": (
        "Vrbo",
        "Vrbo (vrbo.com, Expedia Group's vacation rental site) search, property and suggestions "
        "endpoints; 20 market-languages; billed on actual cost: 2 credits per attempt (a search "
        "usually 2 to 8)."
    ),
    "truecar": (
        "Truecar",
        "TrueCar (truecar.com, the US car-buying marketplace) search, listing, model, reviews, "
        "dealer, dealer_inventory, suggestions, makes and models endpoints; US only, prices in "
        "USD, 1 credit each."
    ),
    "edmunds": (
        "Edmunds",
        "Edmunds (edmunds.com, the US car research and shopping site) search, listing, reviews, "
        "dealer, model, price, appraisal and makes endpoints; US only, prices in USD, 2 credits "
        "each."
    ),
    "kbb": (
        "Kbb",
        "Kelley Blue Book (kbb.com, Cox Automotive's car value and research site) car_value, "
        "model, search, listing, reviews, dealers, dealer and makes_models endpoints; US only, "
        "prices in USD; 1 credit each (a car value at a zip 2, up to 6; deeper review pages up "
        "to 5)."
    ),
    "movoto": (
        "Movoto",
        "Movoto (movoto.com, the US home search site owned by Lower) search, property, "
        "market_trends, suggestions and school endpoints; US only, prices in USD, 1 credit each."
    ),
    "hotpads": (
        "Hotpads",
        "HotPads (hotpads.com, Zillow Group's rental search site) search, listing, "
        "price_history, fees and suggestions endpoints; US rentals, rents in USD, 1 credit each."
    ),
    "apartmentlist": (
        "Apartmentlist",
        "Apartment List (apartmentlist.com, the US rental search site) suggestions, search, "
        "listing, rent_report, market_summary and review_summaries endpoints; US only, rents in "
        "USD, 1 credit each."
    ),
    "compass": (
        "Compass",
        "Compass (compass.com, the US real estate brokerage) search, listing and suggestions "
        "endpoints; homes for sale, for rent and sold across the US, prices in USD, 2 credits "
        "each."
    ),
    "affordablehousing": (
        "Affordablehousing",
        "AffordableHousing.com (affordablehousing.com, the US affordable and Section 8 rental "
        "site) search, listing, suggestions, waiting_lists, housing_authority and "
        "housing_authorities endpoints; US only, rents in USD; search and suggestions 2 credits, "
        "the others 1."
    ),
    "lennar": (
        "Lennar",
        "Lennar (lennar.com, the US homebuilder) search, community, plan, home, master_planned, "
        "markets, market, suggestions, resolve, promotions and payment endpoints; US only, "
        "prices in USD, 1 credit each."
    ),
    "extraspace": (
        "Extraspace",
        "Extra Space Storage (extraspace.com, the US self-storage REIT) search, facility, "
        "reviews, city_prices and locations endpoints; US only, unit prices in USD, 1 credit "
        "each."
    ),
    "publicstorage": (
        "Publicstorage",
        "Public Storage (publicstorage.com, the US self-storage operator, also in Canada) "
        "search, facility and reviews endpoints; market us or ca (English or French), unit "
        "prices in USD or CAD, 1 credit each."
    ),
    "estatesales": (
        "Estatesales",
        "EstateSales.net (estatesales.net, the US estate sale directory) sales, sale, companies, "
        "company, search and item endpoints; US only, prices in USD, 1 credit each."
    ),
    "goodreads": (
        "Goodreads",
        "Goodreads (goodreads.com, Amazon's book community) search, book, reviews, suggestions, "
        "author, author_books, series, editions, list, book_lists, list_search, quotes, genre "
        "and new_releases endpoints; one global English site, 1 credit each."
    ),
    "expedia": (
        "Expedia",
        "Expedia (expedia.com, Expedia Group's travel booking site) search, property, "
        "price_calendar and suggestions endpoints; 51 market-languages (market); billed on "
        "actual cost: 2 credits (1 on some New Zealand, Korea and Indonesia pages)."
    ),
    "academy": (
        "Academy",
        "Academy Sports + Outdoors (academy.com, the US sporting goods retailer) search, "
        "product, store_availability, stores, store, category, categories, deals and suggestions "
        "endpoints; US only, prices in USD (national), exact units per store, 1 credit each."
    ),
    "bathandbodyworks": (
        "Bathandbodyworks",
        "Bath & Body Works (bathandbodyworks.com, the US body care and home fragrance retailer, "
        "and bathandbodyworks.ca) search, category, categories, product, promotions, offers, "
        "store_availability, store, stores and reviews_summary endpoints; country us or ca, "
        "prices in USD or CAD, 1 credit each."
    ),
    "gap": (
        "Gap",
        "Gap Inc. (gap.com: Gap, Old Navy, Banana Republic, Athleta, Gap Factory and Banana "
        "Republic Factory, chosen with brand) search, category, categories, product, prices, "
        "stores, store, store_stock, suggestions, trending and deals endpoints; country us or ca "
        "(English or French), prices in USD or CAD, 1 credit each."
    ),
    "rakuten": (
        "Rakuten",
        "Rakuten (rakuten.com, the cashback site formerly Ebates) stores, store, store_coupons, "
        "rates, search, suggestions, category, deals and in_store endpoints; country us, gb or "
        "ca (English or French), 1 credit each."
    ),
    "bjs": (
        "Bjs",
        "BJ's Wholesale Club (bjs.com, the US warehouse club) product, search, category, "
        "categories, reviews, coupons and clubs endpoints; US only, prices in USD, 1 credit each."
    ),
    "zappos": (
        "Zappos",
        "Zappos (zappos.com, the US shoe and clothing store) and 6pm (6pm.com, its outlet site, "
        "chosen with site) search, product, reviews, questions, lowest_prices, categories and "
        "suggestions endpoints; US only, prices in USD, 1 credit each."
    ),
    "newegg": (
        "Newegg",
        "Newegg (newegg.com, the US computer and electronics store) search, category, "
        "categories, product, offers, reviews, deals, seller, seller_products and suggestions "
        "endpoints; country us, ca or one of 9 Newegg Global storefronts (local currency), 2 "
        "credits each."
    ),
    "rei": (
        "Rei",
        "REI (rei.com, the US outdoor co-op) search, category, deals, product, reviews, "
        "store_stock, stores, store and suggestions endpoints; US only, prices in USD, 2 credits "
        "each."
    ),
}

_HEADER = '''# This file is auto-generated by scripts/gen_namespaces.py from scavio/_spec.py.
# Do NOT edit by hand: edit the spec and re-run `python scripts/gen_namespaces.py`.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, Union

if TYPE_CHECKING:
    from .{client_module} import {client_class}

'''


def _class_name(namespace: str, is_async: bool) -> str:
    base = _NS_META[namespace][0]
    return f"_Async{base}Namespace" if is_async else f"_{base}Namespace"


def _signature_lines(ep: Endpoint) -> list[str]:
    """Build the multi-line parameter list (one param per line, 8-space indent)."""
    lines = ["        self,"]
    for p in ep.required_params:
        lines.append(f"        {p.name}: {p.annotation},")
    for p in ep.positional_optional_params:
        lines.append(f"        {p.name}: {p.annotation} = None,")
    optional = ep.optional_params
    if optional:
        lines.append("        *,")
        for p in optional:
            lines.append(f"        {p.name}: {p.annotation} = None,")
    if ep.http != "GET":
        lines.append("        **extra: Any,")
    return lines


def _docstring_lines(ep: Endpoint) -> list[str]:
    out = [f'        """{ep.summary}', ""]
    if ep.http == "GET":
        out.append("        No API key required. Returns the API response as a dict.")
    elif ep.credits_note:
        # Body-priced surfaces (walmart, threads, kuaishou, extract): the real
        # cost is a function of the request body, so the flat line below would
        # be wrong by up to 40x. credits_note is a complete sentence.
        out.extend(
            f"        {line}"
            for line in textwrap.wrap(
                f"{ep.credits_note} Returns the API response as a dict.", width=88
            )
        )
    else:
        plural = "s" if ep.credits != 1 else ""
        out.append(
            f"        Costs {ep.credits} credit{plural}. Returns the API response as a dict."
        )
    if ep.params or ep.http != "GET":
        out.append("")
        out.append("        Args:")
        for p in ep.params:
            out.append(f"            {p.name}: {p.doc}")
        if ep.http != "GET":
            out.append(
                "            extra: Additional wire parameters passed through verbatim."
            )
    out.append('        """')
    return out


def _method_lines(ep: Endpoint, is_async: bool) -> list[str]:
    kw = "async def" if is_async else "def"
    lines = [f"    {kw} {ep.method}("]
    lines.extend(_signature_lines(ep))
    lines.append("    ) -> dict[str, Any]:")
    lines.extend(_docstring_lines(ep))

    values = "{" + ", ".join(f'"{p.name}": {p.name}' for p in ep.params) + "}"
    call = f'self._client._call("{ep.key}", {values}, extra)'
    if ep.http == "GET":
        call = f'self._client._call("{ep.key}", {{}}, {{}})'
    lines.append(f"        return {'await ' if is_async else ''}{call}")
    return lines


def _class_lines(namespace: str, is_async: bool) -> list[str]:
    name = _class_name(namespace, is_async)
    _, description = _NS_META[namespace]
    client_class = "AsyncScavioClient" if is_async else "ScavioClient"

    lines = [f"class {name}:", f'    """{description}"""', ""]
    lines.append(f'    def __init__(self, client: "{client_class}") -> None:')
    lines.append("        self._client = client")
    for ep in endpoints_for(namespace):
        lines.append("")
        lines.extend(_method_lines(ep, is_async))
    return lines


def render(is_async: bool) -> str:
    client_class = "AsyncScavioClient" if is_async else "ScavioClient"
    client_module = "_async_client" if is_async else "_client"
    parts = [_HEADER.format(client_module=client_module, client_class=client_class)]

    class_names = [_class_name(ns, is_async) for ns in NAMESPACES]
    parts.append("__all__ = [\n" + "".join(f'    "{c}",\n' for c in class_names) + "]\n")

    for ns in NAMESPACES:
        parts.append("\n" + "\n".join(_class_lines(ns, is_async)) + "\n")
    return "".join(parts)


def target_path(is_async: bool) -> Path:
    fname = "_namespaces_async.py" if is_async else "_namespaces_sync.py"
    return _PKG_ROOT / "scavio" / fname


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the generated files are stale instead of writing them.",
    )
    args = parser.parse_args()

    stale = False
    for is_async in (False, True):
        path = target_path(is_async)
        content = render(is_async)
        if args.check:
            current = path.read_text() if path.exists() else ""
            if current != content:
                stale = True
                print(f"stale: {path}")
        else:
            path.write_text(content)
            print(f"wrote: {path}")

    if args.check and stale:
        print("Generated namespace files are out of date. Run: python scripts/gen_namespaces.py")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
