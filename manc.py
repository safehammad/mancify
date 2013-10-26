words = [
    (("acceptable","ace","awesome","brilliant","excellent","fantastic","good",
            "great","likable","lovely","super","smashing","nice","pleasing",
            "rad","superior","worthy","admirable","agreeable","commendable",
            "congenial","deluxe","honorable","honourable","neat","precious",
            "reputable","splendid","stupendous","exceptional","favorable",
            "favourable","marvelous","satisfactory","satisfying","valuable",
            "wonderful","fine","perfect","special","exciting","amazing",),
        ("buzzin'","top","mint","boss","sound","fit","sweet","madferit","safe",)),
    (("anything",),
        ("owt",)),
    (("nothing","none","zero","blank","null","void","nought",),
        ("nowt",)),
    (("disappointed","unhappy","sad","melancholy",),
        ("gutted",)),
    (("break","damage","smash","crack","destroy","annihilate","obliterate",
            "corrupt","ruin","spoil","wreck","trash",),
        ("knacker","bugger",)),
    (("bad","poor","rubbish","broken","errored","damaged","atrocious","awful",
            "cheap","crummy","dreadful","lousy","rough","unacceptable",
            "garbage","inferior","abominable","amiss","beastly","careless",
            "cheesy","crap","crappy","cruddy","defective","deficient",
            "erroneous","faulty","incorrect","inadequate","substandard",
            "unsatisfactory","dysfunctional","malfunctioning","corrupt",),
        ("naff","shit","knackered","buggered","pants","pear-shaped","minging",)),
    (("very","exceedingly","mostly","sheer","exceptionally","genuinely",
            "especially",),
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
        ("minging","rancid",)),
    (("fast","quick","swift","brief",),
        ("rapid",)),
    (("pound",),
        ("quid","squid",)),
    (("hello","greetings","welcome","hi","howdy",),
        ("arrite","how do","hiya",)),
    (("bye","goodbye","farewell",),
        ("ta-ra",)),
    (("kiss",),
        ("snog",)),
    (("food","sustinance",),
        ("scran",)),
    (("eat","consume","absorb","digest",),
        ("scran",)),
    (("you",),
        ("youse",)),
    (("idiot","moron","fool","buffoon","clown","jerk","nerd","nitwit","stooge",
            "sucker","twit","clod","cretin","dolt","dope","dunce","oaf","twerp",
            "imbecile","ignoramus","loon","ninny","numskull",),
        ("scrote","muppet",)),
    (("police","law","cop","cops","policeman","policewoman","constable","officer",
            "detective","bobby","copper",),
        ("dibble",)),
    (("house","dwelling","appartment","building","home","mansion","residence",
            "shack","abode","castle","cave","coop","flat","habitation","pad",
            "residency","place",),
        ("gaff",)),
]


def replace_random(word):
    """Replace given word with a random Mancunian alternative.

    If a replacement word does not exist, return the original word.

    """
    for patterns, replacements in words:
        for pattern in patterns:
            if word == pattern:
                return random.choice(replacements)

    # No replacement found
    return word


if __name__ == "__main__":
	import re,random,sys
	text = sys.argv[1]
	for patts,repls in words:
		for patt in patts:
			text = re.sub(r'\b'+patt+r'\b',lambda m: random.choice(repls),text)
	print text
