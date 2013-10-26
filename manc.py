words = [
	(("acceptable","ace","awesome","brilliant","excellent","fantastic","good",
			"great","likable","lovely","super","smashing","nice","pleasing",
			"rad","superior","worthy","admirable","agreeable","commendable",
			"congenial","deluxe","honorable","honourable","neat","precious",
			"reputable","splendid","stupendous","exceptional","favorable",
			"favourable","marvelous","satisfactory","satisfying","valuable",
			"wonderful","fine","perfect","special",),
		("buzzin'","top","mint","boss","sound","fit")),
	(("anything",),
		("owt",)),
	(("nothing","none","zero","blank","null","void","nought",),
		("nowt",)),
	(("break",),
		("knacker",)),
	(("bad","poor","rubbish","broken","errored","damaged","atrocious","awful",
			"cheap","crummy","dreadful","lousy","rough","sad","unacceptable",
			"garbage","inferior","abominable","amiss","),
		("naff","shit","knackered",)),
	(("very","exceedingly","mostly","sheer",),
		("well","bare","pure",)),
	(("numerous","many","all","most",),
		("bare","pure",)),
	(("mad","crazy","insane","crazed",),
		("barmy",)),
	(("delighted","pleased","happy",),
		("chuffed",)),
	(("things",),
		("shit",)),
	(("attractive",),
		("fit",)),
]


if __name__ == "__main__":
	import re,random,sys
	text = sys.argv[1]
	for patts,repls in words:
		for patt in patts:
			text = re.sub(r'\b'+patt+r'\b',lambda m: random.choice(repls),text)
	print text
