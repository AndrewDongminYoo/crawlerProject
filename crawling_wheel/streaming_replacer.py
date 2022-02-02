import re

from pymongo import MongoClient

client = MongoClient()
db = client.get_database("cat")
col_from = db.get_collection("CatFood_test006")
col_to = db.get_collection("CatFood_test007")
reg_analysis = re.compile(
    "([a-zA-Z1-9가-힣\(\)\-,\*\+\/\s]+)[:]* ([0-9,\.]+\s*(?:\%|mg|IU|mg\/kg|IU\/kg|CFU\/lb|kcal\/2\.47oz|kcal\/kg|kcal\/can)*)")


def analysis_template(string):
    nutrient = {
        "\n": " ",
        "  ": " ",
        "Not Less Than": "",
        "Not More Than": "",
        "(\d\d\.\d kcal) ME\/2\.47oz\.( can)*": "\\1/2.47oz",
        "Energy\: Kcal\/2\.47 oz ([\d\.]+)": "\\1 kcal/2.47oz",
        "Energy\: Kcal\/70 g \(2\.47oz\) ([\d\.]+)": "\\1 kcal/2.47oz",
        "Energy\: Kcal\/70 g\/([\d\.]+)": "\\1 kcal/2.47oz",
        "Omega \– (6|3)(?:\*)* ([\d\.]+)%": "Omega-\\1 \\2 %",
        "total sugar: n\.d\.": "",
        "([ﬁa-zA-Z1-9가-힣†\(\)\-,\*\s]+)[:]* (\%|mg|IU|mg\/kg|IU\/kg|CFU\/lb)+ ([0-9,\.]+)\s([0-9,\.]+)": "\\1: \\3\\2",
        "ﬁ": "fi",
        "é": "e",
        "ï": "i",
        "†": "",
        "Ω": "omega",
        "([ﬁa-zA-Z1-9가-힣†\(\)\-,\*\s]+)[:]* (\%|mg|IU|mg\/kg|IU\/kg|CFU\/lb)+ ([0-9,\.]+)": "\\1: \\3\\2",
        "Not recognized as an essential nutrient by the AAFCO (Cat|Dog) Food Nutrient Profiles\.": "",
        "\(min\.\)\*\*": "",
        "GUARANTEED ANALYSIS\: ": "",
        "KCAL": "kcal",
        "Kcal": "kcal",
        "KG": "kg",
        "Kg": "kg",
        "CAN": "can",
        "CUP": "cup",
        "Vit.": "Vitamin",
        "^\s": "",
        "Guaranteed Analysis": "",
        "Calorie Content": "",
        "\.\*": "",
        "\*": "",
        "Stärke\:": "starch",
        "ME \(Calculated\) \= ": "",
        "\(entire\) ": "",
        "\(Min\.\) ": "",
        "\: \((Lactobacillus acidophilus, Enterococcus faecium)\)": "\\1:",
        "\s{2,}": " ",
        "ANALYTICAL CONSTITUENTS": "",
        "NUTRIENT Carna4 Cat \– Fish Carna4 Cat \– Chicken AAFCO Adult Cat AAFCO Growth Cat AAFCO": "",
        "factory registration number and best before date\: see information on packaging\. To be stored in a cool": "",
        "dry place": "",
        "Nutrient Dry Matter1 \%": "",
        "ANALYTICAL CONSTITUENTS\: ": "",
        "Nutritional additives\: ": "",
        "^3b\d{3} \((\w+)\)": "\\1",
        "Crude Oil \& Fats ": "Crude Fat",
        "Crude Oils \& Fats ": "Crude Fat",
        "Crude oils \& fats": "Crude Fat",
        "Crude oils & Fats": "Crude Fat",
        "Analytical Constituents\: ": "",
        " As Fed": "",
        " \– ": ": ",
        " \— ": ": ",
        "n\.d\.": "0",
        "Calorie Distribution": "",
        "Nutritional Supplements\s*Per 100g\: ": "",
        "Nutrient Analysis": "",
        "Ratio n\-3\:n\-6 1\:\d+ 1\:\d+": "",
        "kcal ME\/2\.47oz": "kcal/2.47oz",
        "\((mg\/kg)\) ([\d,]+)": "\\2 \\1",
        "^\s+": "",
        "Nutritional Info \(Analytical Constituents\)\: ": "",
        "^WEIGHT OF CAT \(LBS\)10 \- 15 [\d\D]+$": "",
        "\(Lactobacillus Acidophilus, Enterococcus Faecium, Lactobacillus Casei\) ": "",
        "Contains a source of live \(viable\) naturally occurring microorganisms\.": "",
        "\: \- ": "",
        "kcal\/100 g": "kcal/100g",
        "Additives\/kg Nutritional Additives\: ": "",
        "Analytical Components\: ": "",
        "\.$": "",
        "Analytical constituents\: ": "",
        "Total Microorganisms: ": "",
        "Total Microorganisms": "",
        " \(min\…$": " ",
        "…": " ",
        " \/ ": "/",
        " million": "000,000",
        "([a-z][:]*)(\d)": "\\1 \\2",
        "  ": " ",
        "[\d\D]+this nutrient is not recognized as an essential nutrient by the AAFCO Cat Nutrient Profiles$": "",
        "^: ": "",
        " \%\: ": ": ",
        " \(min\.\)": "",
        "Calorie Count \(ME Calculated\)\:": "",
        "Contains a source of viable naturally occurring microorganisms": "",
        "([a-zA-Z1-9가-힣†\(\)\-,\*\+\/\s]+) \(([0-9\’,\.]+\s*(?:\%|mg|IU|mg\/kg|IU\/kg|CFU\/lb|kcal\/2\.47oz|kcal\/kg|kcal\/can)*)\)": "\\1 \\2",
        "(\d),(\d{3})": "\\1\\2",
        "^(\d+),(\d{,2})": "\\1.\\2",
        "(Vitamin D3) I\.U\. (\d+)": "\\2 \\1 IU/kg",
        "^(\d{3}) \| \d{3} kcal\/\d{3}g can$": "\\1 kcal/kg",
        "(^\d{4} kcal\/kg), d\+ kcal\/Can 3oz\. \(\d+g\), \d+ kcal\/Can 5\.5oz\. \(\d+g\)$": "\\1",
        "^Carbs NA$": "",
        "^(Vitamin [A-Z0-9])+ \((\d{3,}) I\.U\/kg\)$": "\\1 \\2 IU/kg",
        "^Metabolisable energy\: (MJ|kcal)\/100g ([\d\.]+)$": "calorie: \\2 \\1/100g",
        "^(\d{4} kcal\/kg), \d+ kcal\/Can 3oz\. \(\d+g\), \d+ kcal\/Can 5\.5oz\. \(\d+g\)$": "\\1",
        "^Vitamin D3 \((\d{3,}) I\.U\/kg\)$": "\\1 IU/kg",
        "^Vitaminmin (?:A|E)\. (\d{3,} IU\/kg)$": "\\1",
        "^(Taurine)\. (\d{3,} mg\/kg)$": "\\1 \\2",
        "^[\d\.]+\%$": "",
        "^[\d\.]+ IU\/kg$": "",
        "^(kcal\/100g) (\d{3,})$": "calorie: \\2 \\1",
        "^(\d{3,}) Vitamin D3 IU\/kg$": "Vitamin D3 \\1 IU/kg",
        "^(\d{3,}) kcal\/kg$": "calorie: \\1 kcal/kg",
        "^ME kcal\/100g ([\d\.]+)$": "calorie: \\1 kcal/100g",
    }
    for _from, _to in nutrient.items():
        string = re.sub(_from, _to, string)
    return string.strip()


def key_extractor(string):
    string = string.lower()
    replace_string = {
        "^\(enterococcus faecium, bacillus coagulans, lactobacillus delbrueckii, streptococcus thermophilus, bacillus licheniformis, bacillus subtilis, lactobacillus acidophilus, lactobacillus casei\)$": "microorganisms",
        "^\(lactobacillus casei, lactobacillus$": "microorganisms",
        "^\(lactobacillus plantarum, bacillus subtilis, lactobacillus acidophilus, enterococcus faecium, bifidobacterium animalis in descending amounts\)$": "microorganisms",
        "^\(lactobacillus plantarum, bacillus subtilis, lactobacillus acidophilus, enterococcus faecium, bifidobacterium animalis\) not less than$": "microorganisms",
        "^\(metabolizable energy, calculated\)$": "calorie",
        "^\(saccharomyces cerevisiae, lactobacillus acidophilus, enterococcus faecium\)$": "microorganisms",
        "^2 x$": "",
        "^3564 kcal\/kg$": "",
        "^788 kcal\/kg$": "",
        "^824 kcal\/kg$": "",
        "^882 kcal\/kg$": "",
        "^965 kcal\/kg$": "",
        "^985 kcal\/kg, 84 kcal\/can$": "",
        "^age \(months\)1 \-$": "",
        "^age \(months\)5 \-$": "",
        "^age \(months\)9 \-$": "",
        "^age in months1 \-$": "",
        "^age in months5 \-$": "",
        "^age in months9 \-$": "",
        "^alpha linolenic acid \(omega 3\)$": "omega-3",
        "^alpha\-amylase \(aspergillus oryzae, trichoderma reesei, and rhizopus oryzae\)3$": "amylase",
        "^alpha\-linolenic \(ala\)$": "omega-3",
        "^analytical constituents crude protein$": "crude protein",
        "^ara$": "arachidonic acid",
        "^arachidonic \(aa\)$": "arachidonic acid",
        "^arginine$": "arginine",
        "^ascorbic acid$": "vitamin c",
        "^ascorbic acid \(vitamin c\)$": "vitamin c",
        "^ascorbic acid \(vitaminmin c\)$": "vitamin c",
        "^ash$": "crude ash",
        "^ash maximum$": "crude ash",
        "^ash, not more than$": "crude ash",
        "^bacillus coagulans$": "bacillus coagulans",
        "^barrel$": "",
        "^biotin \(b\-7\)$": "biotin",
        "^biotin \(vitaminmin b7\)$": "biotin",
        "^cal\/phos$": "ca/p ratio",
        "^calcium$": "calcium",
        "^calcium \(\)$": "calcium",
        "^calcium \(ca\)$": "calcium",
        "^calcium g$": "calcium",
        "^calcium g 1,15$": "calcium",
        "^calcium minimum$": "calcium",
        "^calcium not lessthan$": "calcium",
        "^calcium\/phosphorous ratio$": "ca/p ratio",
        "^calcium\/phosphorus ratio$": "ca/p ratio",
        "^carbohydrate g \(nfe\)$": "carbohydrate",
        "^carbohydrate g \(nfe\) 38,1$": "carbohydrate",
        "^carbohydrates$": "carbohydrate",
        "^carbs$": "carbohydrate",
        "^cellulase \(aspergillus oryzae, trichoderma reesei, and rhizopus oryzae\)2$": "cellulase",
        "^chondroitin sulfate$": "chondroitin",
        "^chondroitin sulfate $": "chondroitin",
        "^chondroitin sulphate$": "chondroitin",
        "^chondrotin sulfate$": "chondroitin",
        "^cobalamin \(vitaminmin b12\)$": "vitamin b12",
        "^contains natural anti\-oxidants and$": "",
        "^copper \(cu\)$": "copper",
        "^copper \(ppm\)$": "copper",
        "^copper proteinate$": "copper",
        "^copper sulphate$": "copper",
        "^crude ber$": "crude fiber",
        "^crude fa$": "crude fat",
        "^crude fat \(\)$": "crude fat",
        "^crude fat \(min\)$": "crude fat",
        "^crude fat minimum$": "crude fat",
        "^crude fat\(min\)$": "crude fat",
        "^crude fat,$": "crude fat",
        "^crude fat, not less than$": "crude fat",
        "^crude fats$": "crude fat",
        "^crude fiber$": "crude fiber",
        "^crude fiber \(\)$": "crude fiber",
        "^crude fiber \(max\)$": "crude fiber",
        "^crude fiber\(max\)$": "crude fiber",
        "^crude fiber,$": "crude fiber",
        "^crude fiber, not more than$": "crude fiber",
        "^crude fibers$": "crude fiber",
        "^crude fibre$": "crude fiber",
        "^crude fibres$": "crude fiber",
        "^crude moisture\(max\)$": "moisture",
        "^crude oil and fats$": "crude fat",
        "^crude oils and fats$": "crude fat",
        "^crude protein$": "crude protein",
        "^crude protein \(\)$": "crude protein",
        "^crude protein \(min\)$": "crude protein",
        "^crude protein minimum$": "crude protein",
        "^crude protein\(min\)$": "crude protein",
        "^crude protein,$": "crude protein",
        "^crude protein, not less than$": "crude protein",
        "^crude proteins$": "crude protein",
        "^crude protien$": "crude protein",
        "^crudeprotein$": "crude protein",
        "^cu$": "copper",
        "^cude fiber$": "crude fiber",
        "^cystine$": "cystine",
        "^dha$": "DHA",
        "^dha \(docosahexaenoic acid\)$": "DHA",
        "^dha \(docosohexaenoic acid\)$": "DHA",
        "^dha \+ epa$": "DHA\+EPA",
        "^dha g$": "DHA",
        "^digestibility$": "",
        "^dihomo\-gamma linolenic \(dgla\)$": "GLA",
        "^dl\-methionine$": "dl\-methionine",
        "^docosahexaenoic \(dha\)$": "DHA",
        "^docosahexaenoic acid \(dha\)$": "DHA",
        "^docosahexaenoic acid \(dha\) \(\)$": "DHA",
        "^dry matter$": "",
        "^eicosapentaenoic \(epa\)$": "EPA",
        "^eicosapentaenoic \+ docosahexaenoic acid$": "DHA+EPA",
        "^eicosapentaenoic acid \(epa\)$": "EPA",
        "^eliadic$": "",
        "^energy$": "calorie",
        "^epa$": "EPA",
        "^epa \(eicosapentaenoic acid \)$": "EPA",
        "^epa \(eicosapentaenoic acid\)$": "EPA",
        "^epa \+ dha$": "DHA\+EPA",
        "^epa g$": "EPA",
        "^erucic$": "",
        "^fat$": "crude fat",
        "^fat \(acid hydrolysis\)$": "crude fat",
        "^fat content$": "crude fat",
        "^fat g \(crude\)$": "crude fat",
        "^fats$": "crude fat",
        "^fe$": "ferrous sulphate",
        "^ferrous sulphate$": "ferrous sulphate",
        "^fettgehalt$": "crude fat",
        "^feuchtigkeit$": "moisture",
        "^fiber$": "crude fiber",
        "^fiber \(crude\)$": "crude fiber",
        "^fibers$": "crude fiber",
        "^fibre$": "crude fiber",
        "^fibre g \(crude\)$": "crude fiber",
        "^folic acid$": "folic acid",
        "^folic acid \(b\-9\)$": "folic acid",
        "^folic acid \(vitaminmin b9\)$": "folic acid",
        "^fructo\-oligosaccharides$": "fructo-oligosaccharides",
        "^gamma\-linolenic \(gla\)$": "GLA",
        "^glucosamine$": "glucosamine",
        "^glucosamine $": "glucosamine",
        "^glucosamine hydrochloride$": "glucosamine",
        "^histidine$": "histidine",
        "^i$": "",
        "^inorganic matter$": "",
        "^iodine$": "iodine",
        "^iron$": "iron",
        "^iron \(fe\) 75 mg\/kg copper \(cu\)$": "copper",
        "^iron proteinate$": "iron",
        "^isoleucine$": "isoleucine",
        "^kalium$": "potassium",
        "^kcal\/$": "calorie",
        "^kcal\/oz\(calculated\)$": "kcal/oz",
        "^kilocalories$": "calorie",
        "^l carnitine$": "l-carnitine",
        "^l\-carnitine$": "l-carnitine",
        "^l\-carnitine \(min\)$": "l-carnitine",
        "^l\-carntine$": "l-carnitine",
        "^lactobacillus acidophilus$": "lactobacillus acidophilus",
        "^leucine$": "leucine",
        "^linoleic \(la\)$": "omega-6",
        "^linoleic a$": "omega-6",
        "^linoleic acid$": "omega-6",
        "^linoleic acid \(omega 6\)$": "omega-6",
        "^linoleic acid minimum$": "omega-6",
        "^linolenic a$": "omega-6",
        "^linolenic acid$": "omega-6",
        "^lysine$": "l\-lysine",
        "^maganese$": "manganese",
        "^magnesium$": "magnesium",
        "^magnesium $": "magnesium",
        "^magnesium \-$": "magnesium",
        "^magnesium g$": "magnesium",
        "^magnesium maximum$": "",
        "^manganese$": "manganese",
        "^manganese \(mn\)$": "manganese",
        "^manganese proteinate$": "manganese",
        "^manganous oxide$": "manganese",
        "^mannan\-oligosaccharides$": "mannan-oligosaccharides",
        "^maximum crude fibre$": "crude fiber",
        "^maximum fiber$": "crude fiber",
        "^maximum moisture$": "moisture",
        "^me$": "calorie",
        "^me \(calculated\)$": "calorie",
        "^me 1118 kcal\/kg,$": "calorie",
        "^me 1135 kcal\/kg,$": "calorie",
        "^me 1141 kcal\/kg,$": "calorie",
        "^me 1253 kcal\/kg,$": "calorie",
        "^me 1287 kcal\/kg,$": "calorie",
        "^me 875 kcal\/kg,$": "calorie",
        "^me 912 kcal\/kg,$": "calorie",
        "^me 916 kcal\/kg,$": "calorie",
        "^me 942 kcal\/kg,$": "calorie",
        "^me 953 kcal\/kg,$": "calorie",
        "^me kcal\/kg$": "calorie",
        "^me\(kcal\/kg\)$": "calorie",
        "^metabolisable energy$": "calorie",
        "^metabolisable energy \(atwater calculation\)$": "calorie",
        "^methionine$": "dl\-methionine",
        "^methionine\-cystine$": "methionine-cystine",
        "^mg\/kg taurine$": "taurine",
        "^microorganismslactobacillus acidophilus, enterococcus faecium$": "microorganisms",
        "^min omega\-3 fatty acids$": "omega-3",
        "^minerals$": "minerals",
        "^minerals \(mg per kg\) iron$": "iron",
        "^minimum crude fat$": "crude fat",
        "^minimum crude protein$": "crude protein",
        "^minimum fat$": "crude fat",
        "^minimum protein$": "crude protein",
        "^minimum taurine$": "taurine",
        "^mn$": "manganese",
        "^moisture$": "moisture",
        "^moisture \(\)$": "moisture",
        "^moisture \(max\)$": "moisture",
        "^moisture,$": "moisture",
        "^moisture, not more than$": "moisture",
        "^moisturmaximum$": "moisture",
        "^monounsaturated fats$": "crude fat",
        "^msm$": "MSM",
        "^n\-3 fatty acids$": "omega-3",
        "^n\-6 fatty acids$": "omega-6",
        "^natrium$": "sodium",
        "^nfe$": "carbohydrate",
        "^niacin$": "niacin",
        "^niacin \(b\-3\)$": "niacin",
        "^niacin \(vitaminmin b3\)$": "niacin",
        "^oleic$": "oleic acid",
        "^omega$": "omega-3",
        "^omega 3$": "omega-3",
        "^omega 3 \(linolenic acid\)$": "omega-3",
        "^omega 3 fatty acids$": "omega-3",
        "^omega 6$": "omega-6",
        "^omega 6 \(linoleic acid\)$": "omega-6",
        "^omega 6 fatty acids$": "omega-6",
        "^omega 9 fatty acids$": "omega-9",
        "^omega\-3$": "omega-3",
        "^omega\-3 fats$": "omega-3",
        "^omega\-3 fatty acid$": "omega-3",
        "^omega\-3 fatty acid \(\)$": "omega-3",
        "^omega\-3 fatty acids$": "omega-3",
        "^omega\-3 fatty acids \(min\)$": "omega-3",
        "^omega\-3 fatty acids g$": "omega-3",
        "^omega\-3 fatty acids\(min\)$": "omega-3",
        "^omega\-3\-fatty acids$": "omega-3",
        "^omega\-6$": "omega-6",
        "^omega\-6 fatty acid$": "omega-6",
        "^omega\-6 fatty acid \(\)$": "omega-6",
        "^omega\-6 fatty acids$": "omega-6",
        "^omega\-6 fatty acids \(min\)$": "omega-6",
        "^omega\-6 fatty acids\(min\)$": "omega-6",
        "^omega\-6\-fatty acids$": "omega-6",
        "^omega\-9 fatty acids$": "omega-9",
        "^ounces per cup$": "",
        "^pantothenic acid$": "pantothenic acid",
        "^pantothenic acid \(b\-5\)$": "pantothenic acid",
        "^pantothenic acid \(vitaminmin b5\)$": "pantothenic acid",
        "^pfc$": "PFC",
        "^ph$": "pH",
        "^phenylalanine$": "phenylalanine",
        "^phenylalanine\-tyrosine$": "phenylalanine\-tyrosine",
        "^phosphor$": "phosphorous",
        "^phosphorous$": "phosphorous",
        "^phosphorus$": "phosphorous",
        "^phosphorus \(\)$": "phosphorous",
        "^phosphorus g$": "phosphorous",
        "^phosphorus minimum$": "phosphorous",
        "^polyunsaturated fats$": "polyunsaturated fats",
        "^potassium$": "potassium",
        "^potassium g$": "potassium",
        "^potassium iodide$": "potassium",
        "^protease \(aspergillus oryzae, trichoderma reesei, and rhizopus oryzae\)$": "protease",
        "^protease \(aspergillus oryzae, trichoderma reesei, and rhizopus oryzae\)1$": "protease",
        "^protein$": "crude protein",
        "^protein \(crude\)$": "crude protein",
        "^protein g \(crude\)$": "crude protein",
        "^pyridoxine$": "pyridoxine",
        "^pyridoxine \(b\-6\)$": "pyridoxine",
        "^pyridoxine \(vitaminmin b6\)$": "pyridoxine",
        "^raw ash$": "crude ash",
        "^raw fibre$": "crude fiber",
        "^retinol \(vitaminmin a\)$": "vitamin a",
        "^riboflavin$": "riboflavin",
        "^riboflavin \(b\-2\)$": "riboflavin",
        "^riboflavin \(vitaminmin b2\)$": "riboflavin",
        "^rohasche$": "crude ash",
        "^rohfaser$": "crude fiber",
        "^rohprotein$": "crude protein",
        "^saturated fat$": "saturated fat",
        "^schwefel$": "sulfur",
        "^se$": "selenium",
        "^selenium$": "selenium",
        "^selenium minimum$": "selenium",
        "^sodium$": "sodium",
        "^sodium $": "sodium",
        "^sodium g$": "sodium",
        "^sodium minimum$": "sodium",
        "^starch$": "starch",
        "^starch \($": "starch",
        "^sulfur$": "sulfur",
        "^sulphur$": "sulfur",
        "^taurin$": "taurine",
        "^taurine$": "taurine",
        "^taurine \(\)$": "taurine",
        "^taurine \(as received, typical analysis\)$": "taurine",
        "^taurine \(extruded\)$": "taurine",
        "^taurine \(min\)$": "taurine",
        "^taurine total$": "taurine",
        "^thiamin \(b1\)$": "thiamine",
        "^thiamine$": "thiamine",
        "^thiamine hydrochloride \(vitaminmin b1\)$": "thiamine",
        "^this food contains 3451 kcal\/kg or$": "3451 kcal\/kg",
        "^this food contains 3561 kcal\/kg or$": "3561 kcal\/kg",
        "^threonine$": "threonine",
        "^total bacillus coagulans fermentation product$": "microorganisms",
        "^total bacillus coagulans fermentation product \(min$": "microorganisms",
        "^total lactic acid microorganisms$": "microorganisms",
        "^total microorganisms$": "microorganisms",
        "^total microorganisms \(lactobacillus acidophilus, lactobacillus plantarum, lactobacillus reuteri, bifidobacterium animalis, enterococcus faecium\) not less than$": "microorganisms",
        "^total microorganisms min$": "microorganisms",
        "^total sugar$": "starch",
        "^trans fatty acids$": "trans fatty acids",
        "^tryptophan$": "tryptophan",
        "^trytophan$": "tryptophan",
        "^tyrosine$": "tyrosine",
        "^valine$": "valine",
        "^vitamin$": "vitamin",
        "^vitamin a$": "vitamin A",
        "^vitamin c$": "vitamin C",
        "^vitamin d$": "vitamin D",
        "^vitamin d3$": "vitamin D3",
        "^vitamin d3 1$": "vitamin D3",
        "^vitamin e$": "vitamin E",
        "^vitamin eminimum$": "vitamin E",
        "^vitamin minimum$": "vitamin",
        "^vitaminmin a$": "vitamin A",
        "^vitaminmin b\-12$": "vitamin B12",
        "^vitaminmin b12$": "vitamin B12",
        "^vitaminmin c$": "vitamin C",
        "^vitaminmin d$": "vitamin D",
        "^vitaminmin d3$": "vitamin D3",
        "^vitaminmin d3 \(cholecalciferol\)$": "vitamin D3",
        "^vitaminmin e$": "vitamin E",
        "^vitaminmin e \(alpha\-tocopherol\)$": "vitamin E",
        "^vitaminmin e \(beta\-tocopherol\)$": "vitamin E",
        "^vitaminmin e \(delta\-tocopherol\)$": "vitamin E",
        "^vitaminmin e \(gamma\-tocopherol\)$": "vitamin E",
        "^vitaminmin e \(min\)$": "vitamin E",
        "^vitaminmin e \(total\)$": "vitamin E",
        "^vitaminmin k$": "vitamin K",
        "^vitaminmina$": "vitamin A",
        "^vitaminminc$": "vitamin C",
        "^vitaminmind$": "vitamin D",
        "^vitaminmine$": "vitamin E",
        "^vitaminmins \(per kg\) vitaminmin a$": "vitamin A",
        "^water$": "moisture",
        "^water content$": "moisture",
        "^water g$": "moisture",
        "^water\-soluble chlorides$": "chloride",
        "^weight of cat \(lbs\)$": "",
        "^weight of cat \(lbs\) 4$": "",
        "^weight of cat \(lbs\) 4 \-$": "",
        "^weight of cat \(lbs\) 4 \- 7 weight of cat \(kg\)2 \-$": "",
        "^weight of cat \(lbs\) 7$": "",
        "^weight of cat \(lbs\) 7 \-$": "",
        "^weight of cat \(lbs\)4 \-$": "",
        "^weight of cat \(lbs\)4 \- 7 weight of cat \(kg\)2 \-$": "",
        "^weight of cat \(lbs\)7 \-$": "",
        "^zin$": "zinc",
        "^zinc$": "zinc",
        "^zinc \(ppm\)$": "zinc",
        "^zinc min$": "zinc",
        "^zn$": "zinc",
        "^글루코사민$": "glucosamine",
        "^나트륨$": "sodium",
        "^단백질$": "crude protein",
        "^단백질질$": "crude protein",
        "^라이신$": "l-lysine",
        "^마그네슘$": "magnesium",
        "^베타카로틴$": "b-carotine",
        "^비타민 a$": "vitamin A",
        "^비타민 c$": "vitamin C",
        "^비타민 d$": "vitamin D",
        "^비타민 e$": "vitamin E",
        "^수분$": "moisture",
        "^인$": "phosphorous",
        "^조단백$": "crude protein",
        "^조단백질$": "crude protein",
        "^조섬유$": "crude fiber",
        "^조지방$": "crude fat",
        "^조회분$": "crude ash",
        "^지방$": "crude fat",
        "^총 omega\-3 지방산$": "omega-3",
        "^총 omega\-6 지방산$": "omega-6",
        "^카르니틴$": "carnitine",
        "^칼륨$": "potassium",
        "^칼슘$": "calcium",
        "^타우린$": "taurine",
        "^탄수화물$": "carbohydrate",
        "^회분$": "crude ash",
    }
    for k, v in replace_string.items():
        string = re.sub(k, v, string)
    return string


def main():
    count = 0
    key_box = []
    for item in col_from.find({}, {"_id": False}):
        analysis = (item.get("analysis"))
        if type(analysis) is str:
            item["analysis"] = None
        else:
            for tem in analysis:
                tem = analysis_template(tem)
                if tem:
                    test = reg_analysis.match(tem)
                    if not test:
                        count += 1
                        # print(tem)
                    else:
                        key, val = test.groups()
                        if key_extractor(key):
                            item[key_extractor(key)] = val
        col_to.update_one({"url": item["url"]}, {"$set": item}, upsert=True)
    print(count)


if __name__ == '__main__':
    main()
