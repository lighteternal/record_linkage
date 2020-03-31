# Record Linkage (Entity Resolution) on eshop product descriptions 
#
#

## Description
Entity resolution on online product descriptions (cameras) from different e-shops (e.g. wallmart, ebay) using distance/similarity measures (e.g. Jaro–Winkler distance)
This proof-of-concept works on JSON files of two e-shops selling cameras. Some (but not all) of the available items are common to both shops but the description structure (fields) is specific to each shop.


Two-step procedure: 
1. Check the available info (description fields) from both eshops and extract similar headers using simiarity measures
2. Perform record linkage on the content of the identified fields to identify links between products of each shop (e.g. productID=13 of shopA is the same with productID=77 of shopB) and return list of possible links.
 
