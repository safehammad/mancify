from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
    )

# Make Py2's str type like Py3's
str = type('')


structure_rules = [
    ((["JJ*","NN*"],),
        (["chuffing",0,1],),
        0.1),
    ((["END"],),
        (["our","kid",0],["init",0],["and","that",0],["and","stuff",0]),
        0.1),
    ((["NN*"],),
        (["thing"],),
        0.1),
    ((["START"],),
        ([0,"here","yar",","],),
        0.1),
]

ignores = [ "i","a" ]

word_rules = [
    (("and",),
        ("n'",)),
    (("of",),
        ("ov",)),
    (("her",),
        ("'er",)),
    (("my",),
        ("me",)),
    (("what",),
        ("wot",)),
    (("our",),
        ("ah",)),
    (("acceptable","ace","awesome","brilliant","excellent","fantastic","good",
            "great","likable","lovely","super","smashing","nice","pleasing",
            "rad","superior","worthy","admirable","agreeable","commendable",
            "congenial","deluxe","honorable","honourable","neat","precious",
            "reputable","splendid","stupendous","exceptional","favorable",
            "favourable","marvelous","satisfactory","satisfying","valuable",
            "wonderful","fine","perfect","special","exciting","amazing","succeeded",
            "worked","successful"),
        ("buzzin'","top","mint","boss","sound","fit","sweet","madferit","safe","raz",
            "bob on","bangin'","peach","bazzin'","kewl","quality")),
    (("anything",),
        ("owt",)),
    (("nothing","none","zero","blank","null","void","nought",),
        ("nowt",)),
    (("disappointed","unhappy","sad","melancholy",),
        ("gutted",)),
    (("break","damage","smash","crack","destroy","annihilate","obliterate",
            "corrupt","ruin","spoil","wreck","trash","fail",),
        ("knacker","bugger",)),
    (("bad","poor","rubbish","broken","errored","damaged","atrocious","awful",
            "cheap","crummy","dreadful","lousy","rough","unacceptable",
            "garbage","inferior","abominable","amiss","beastly","careless",
            "cheesy","crap","crappy","cruddy","defective","deficient",
            "erroneous","faulty","incorrect","inadequate","substandard",
            "unsatisfactory","dysfunctional","malfunctioning","corrupt","failed",),
        ("naff","shit","knackered","buggered","pants","pear-shaped","tits up",
            "ragged","devilled","out of order","bang out of order","biz","kippered",
            "bobbins")),
    (("error","mistake","problem",),
        ("cock up","balls up")),
    (("very","exceedingly","mostly","sheer","exceptionally","genuinely",
            "especially","really"),
        ("well","bare","pure","dead","proper",)),
    (("numerous","many","all","most",),
        ("bare","pure",)),
    (("mad","crazy","insane","crazed","kooky","nuts","nutty","silly","wacky",
            "beserk","cuckoo","potty","batty","bonkers","unhinged","mental",
            "idiotic","stupid","moronic","dumb","foolish",),
        ("barmy",)),
    (("delighted","pleased","happy","cheerful","contented","ecstatic","elated",
            "glad","joyful","joyous","jubilant","lively","merry","overjoyed",
            "peaceful","pleasant","pleased","thrilled","upbeat","blessed",
            "blest","blissful","captivated","gleeful","gratified","jolly",
            "mirthful","playful","proud",),
        ("chuffed","buzzin'")),
    (("things","stuff","elements","parts","pieces","facts","subjects","situations",
            "concepts","concerns","items","materials","objects","files",),
        ("shit",)),
    (("attractive","alluring","beautiful","charming","engaging","enticing",
            "glamorous","gorgeous","handsome","inviting","tempting","adorable",
            "agreeable","enchanting","enthralling","hunky","pretty","seductive",
            "provocative","tantalizing","teasing","stunning",),
        ("fit",)),
    (("any",),
        ("whatever",)),
    (("unattractive","ugly","horrible","nasty","unpleasant","hideous","gross",
            "unsightly","horrid","unseemly","grisly","awful","foul","repelling",
            "repulsive","repugnant","revolting","uninviting","monstrous",),
        ("mingin'","rancid","'angin","rank","manky")),
    (("fast","quick","swift","brief",),
        ("rapid",)),
    (("pound",),
        ("quid","squid",)),
    (("man",),
        ("bloke", "fella",)),
    (("men",),
        ("blokes", "fellas",)),
    (("mate", "friend"),
        ("pal","mate",)),
    (("hello","greetings","welcome","hi","howdy",),
        ("arrite","how do","hiya",)),
    (("bye","goodbye","farewell",),
        ("ta-ra",)),
    (("kiss",),
        ("snog",)),
    (("sandwich",),
        ("butty","barm")),
    (("sandwiches",),
        ("butties","barms")),
    (("eat","consume","absorb","digest","food","sustinance",),
        ("scran",)),
    (("you",),
        ("youse",)),
    (("idiot","moron","fool","buffoon","clown","jerk","nerd","nitwit","stooge",
            "sucker","twit","clod","cretin","dolt","dope","dunce","oaf","twerp",
            "imbecile","ignoramus","loon","ninny","numskull",),
        ("scrote","muppet","knobber","spanner","gonk","cabbage")),
    (("police","law","cop","cops","policeman","policewoman","constable","officer",
            "detective","bobby","copper",),
        ("dibble",)),
    (("house","dwelling","appartment","building","home","mansion","residence",
            "shack","abode","castle","cave","coop","flat","habitation","pad",
            "residency","place",),
        ("gaff",)),
    (("was",),
        ("were",)),
    (("were",),
        ("was",)),
    (("yes","ok",),
        ("aye",)),
    (("are",),
        ("iz",)),
    (("no",),
        ("nah",)),
    (("haven't",),
        ("ain't",)),
    (("right",),
        ("reet",)),
    (("the",),
        ("t'",)),
    (("?",),
        ("eh?","or wot?","? Yeah?")),
]

phoneme_rules = [
    ((["START","HH"],),
        ["START","'"]),
    ((["ER","END"],),
      ["AA","'","END"]),
    ((["T","END"],),
        ["'","END"],),
    ((["AE","R"],),
        ["AE"]),
    ((["AA","R"],),
        ["AE","R"]),
    ((["AO","R","END"],["UH","R","END"],),
        ["AH","R"]),
    ((["AO"],),
        ["AA"],),
    ((["NG","END"],),
        ["N","'","END"]),
    ((["T","UW","END"],),
        ["T","AH","END"]),
    ((["START","DH"],),
        ["START","D"]),
    ((["TH","END"],),
        ["F","END"],),
    ((["DH","END"],),
        ["V","END"],),
    ((["START","TH"],),
        ["START","F"]),
    ((["VOWEL","T","VOWEL"],),
        [0,"R",2]),
]

if __name__ == "__main__":
    import re,random,sys
    text = sys.argv[1]
    for patts,repls in words:
        for patt in patts:
            text = re.sub(r'\b'+patt+r'\b',lambda m: random.choice(repls),text)
    print(text)
