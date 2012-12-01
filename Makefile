all:
	hfst-lexc apertium-khk.khk.lexc -o khk-lexc.hfst
	hfst-twolc apertium-khk.khk.twol -o khk-twol.hfst
	hfst-compose-intersect -1 khk-lexc.hfst -2 khk-twol.hfst -o khk-gen.hfst
	hfst-invert khk-gen.hfst -o khk-mor.hfst
	hfst-fst2fst -O -i khk-gen.hfst -o khk.autogen.hfst
	hfst-fst2fst -O -i khk-mor.hfst -o khk.automorf.hfst
