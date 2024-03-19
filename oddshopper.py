import requests
import webbrowser
import time
import json
import sys
import os
import re
from arb_compute import computeWagers
MIN_PCT = 1.00

def correctForLocation(s):
    if "betmgm.com" in s:
        return s.replace("nj.betmgm.com", "ny.betmgm.com")
    return s

def getJsonAround(text, ind):
    ind1 = ind
    ind2 = ind
    right = 0
    while text[ind1] != '{' or right > 0:
        ind1 -=1
        if text[ind1] == '}':
            right+=1
        if text[ind1] == '{':
            right-=1
    left = 0
    while text[ind2] != '}' or left > 0:
        ind2+=1
        if text[ind2] == '{':
            left+=1
        if text[ind2] == '}':
            left-=1
    ind2+=1
    return json.loads(text[ind1:ind2])


if __name__ == "__main__":
    bookies = sys.argv[1:-1]
    wager = int(sys.argv[-1])
    while True:
        f = open("active_arbs.txt")
        arb_ids = set(list(map(lambda x: x.strip(), f.readlines())))
        f.close()
        r = requests.get("https://www.oddsshopper.com/tools/arbitrage/ny")
        lines = r.text.split("\n")
        i = 0
        while "window.__PRELOADED_STATE" not in lines[i][:50]:
            i+=1
        f = open('t.txt', 'w')
        data = lines[i].strip()
        f.write(data)
        f.close()
        # find all instnces of "sideOneSportsbookCode"
        arb_inds = [m.start() for m in re.finditer("arbitrageId",data)]
        arbs = list(map(lambda x: getJsonAround(data, x), arb_inds))
        # Save only those between the bookies above
        arbs = list(filter(lambda x: x["sideOneSportsbookCode"] in bookies and x["sideTwoSportsbookCode"] in bookies, arbs))
        if len(arbs) > 0:
            # Check if these arbs are different than the ones we have
            new_arbs = []
            f = open("active_arbs.txt", "w")
            for arb in arbs:
                ac = arb.copy()
                ac["arbitrageId"] = ""
                if str(ac) not in arb_ids:
                    new_arbs.append(arb)
                f.write(str(ac) + "\n")
            f.close()
            if len(new_arbs) > 0:
                min_pct_arbs = []
                for i in range(len(new_arbs)):
                    # write arb id to file
                    wagers = computeWagers(new_arbs[i]["sideOneOddsDecimal"], new_arbs[i]["sideTwoOddsDecimal"], wager)
                    new_arbs[i]["wagers"] = wagers
                    if MIN_PCT <= (wagers[0]*new_arbs[i]["sideOneOddsDecimal"] - wager)*100/wager: 
                        print((wagers[0]*new_arbs[i]["sideOneOddsDecimal"] - wager)*100/wager)

                        min_pct_arbs.append(new_arbs[i])

                if len(min_pct_arbs) > 0:
                    os.system("afplay ping.mp3")
                    print("{} new >= {:.3f}% arbs found on OddsShopper from a total of {} active arbs from {}".format(len(min_pct_arbs),MIN_PCT, len(arbs), bookies))

                min_pct_arbs.sort(key = lambda x: x["sideOneOddsDecimal"]*x["wagers"][0], reverse=True)
                for arb in min_pct_arbs:
                    wagers = arb["wagers"]
                    print(correctForLocation(arb["sideOneDeeplinkUrl"]))
                    print(correctForLocation(arb["sideTwoDeeplinkUrl"]))
                    print("{} {} -> {} -> {:.3f}%".format(arb["sideOneOddsAmerican"], arb["sideTwoOddsAmerican"], wagers, (wagers[0]*arb["sideOneOddsDecimal"] - wager)*100/wager))
                    print()
        time.sleep(1)

      
    
