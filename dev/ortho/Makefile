all: cyr-ipa.ohfst

cyr-ipa: cyr-ipa.ohfst

# create full transcription transducer from lexc and twol transducers
cyr-ipa.hfst: cyr-ipa.twol.hfst cyr-ipa.lexc.hfst
	hfst-compose-intersect -1 cyr-ipa.lexc.hfst -2 cyr-ipa.twol.hfst -o cyr-ipa.hfst

# create transcription transducer optimised-lookup format
cyr-ipa.ohfst: cyr-ipa.hfst
	hfst-fst2fst -w -i $< -o $@

cyr-ipa.lexc.hfst: cyr-ipa.lexc
	hfst-lexc $< -o $@

cyr-ipa.twol.hfst: cyr-ipa.twol
	hfst-twolc $< -o $@

clean:
	rm -rf *.ohfst *.hfst
