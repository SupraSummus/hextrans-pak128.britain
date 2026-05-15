# Just run
#   make clean all archives
# to get fresh and ready to deploy .tbz2 and .zip archives
#
# Change THIS to change the version string encoded in the pak file
# VERSION_STRING = "pak128.Britain-Ex-0.9.4"
#
#
#
MAKEOBJ ?= ./makeobj-extended

DESTDIR  ?= build
PAKDIR   ?= $(DESTDIR)/pak128.Britain-Ex
DESTFILE ?= simupak128.Britain-Ex

# Dirs for simutranslator
# Build scope is two-layered:
#
# * Category gate (the `DIRS* += <dir>` lines below): which dirs the
#   build visits at all.  A category with no ports yet stays
#   commented out — visiting it would generate an empty .pak with
#   no contents.
#
# * File filter (the `ported_dats` function): within a visited dir,
#   only `.dat` files with a sibling `.png` reach makeobj.  Lets a
#   partly-ported category (e.g. `trains/` with 4 ports against 866
#   unported upstream dats) build cleanly without bulk-stripping
#   the unported reference dats.
#
# See TODO.md -> "Expand build scope as categories bake".
TR_DIRS :=

OUTSIDE :=
#OUTSIDE += pak1file/128
#TR_DIRS += pak1file/128

DIRS32 :=
#DIRS32 += boats/holds
#TR_DIRS += boats/holds

DIRS64 :=
#DIRS64 += gui/gui64
#TR_DIRS += gui

DIRS128 :=
DIRS128 += air
TR_DIRS += air
#DIRS128 += attractions
#TR_DIRS += attractions
#DIRS128 += boats
#TR_DIRS += boats
#DIRS128 += bus
#TR_DIRS += bus
#DIRS128 += citybuildings
#TR_DIRS += citybuildings
#DIRS128 += citycars
#TR_DIRS += citycars
#DIRS128 += depots
#TR_DIRS += depots
#DIRS128 += goods
#TR_DIRS += goods
DIRS128 += grounds
TR_DIRS += grounds
#DIRS128 += gui/gui128
#DIRS128 += hq
#TR_DIRS += hq
#DIRS128 += industry
#TR_DIRS += industry
#DIRS128 += london-underground
#TR_DIRS += london-underground
#DIRS128 += maglev
#TR_DIRS += maglev
#DIRS128 += narrowgauge
#TR_DIRS += narrowgauge
#DIRS128 += pedestrians
#TR_DIRS += pedestrians
#DIRS128 += smokes
#TR_DIRS += smokes
#DIRS128 += stations
#TR_DIRS += stations
#DIRS128 += signalboxes
#TR_DIRS += signalboxes
#DIRS128 += townhall
#TR_DIRS += townhall
DIRS128 += trains
TR_DIRS += trains
DIRS128 += trams
TR_DIRS += trams
#DIRS128 += trees
#TR_DIRS += trees
DIRS128 += ways
TR_DIRS += ways
#DIRS128 += piers
#TR_DIRS += piers

DIRS192 :=
#DIRS192 += boats/boats192
#DIRS192 += air/air192

DIRS224 :=
#DIRS224 += boats/boats224

DIRS256 :=
#DIRS256 += air/air256

DIRS := $(OUTSIDE) $(DIRS32) $(DIRS64) $(DIRS128) $(DIRS192) $(DIRS224) $(DIRS256)

#generating filenames
#with this function the filenames are assembled, by removing the dir
make_name = $(subst /,.,$1).pak

# Filter to the .dat files in a directory that have a sibling .png —
# i.e. ported assets (bake-unit triple) or carry-over authored
# pairs.  Unported upstream .dats (no .png) stay in the tree as
# seeder input for `port_vehicle` but don't enter the build.  See
# CLAUDE.md -> "Bake units and per-asset layout".
ported_dats = $(foreach d,$(wildcard $1/*.dat),$(if $(wildcard $(d:.dat=.png)),$(d),))

.PHONY: $(DIRS) copy tar zip simutranslator

all: copy $(DIRS)

archives: tar zip

tar: $(DESTFILE).tbz2
zip: $(DESTFILE).zip

$(DESTFILE).tbz2: $(PAKDIR)
	@echo "===> TAR $@"
	@tar cjf $@ -C $(DESTDIR) $(notdir $(PAKDIR))

$(DESTFILE).zip: $(PAKDIR)
	@echo "===> ZIP $@"
	@rm -f $@
	@cd $(DESTDIR) && zip -rq $(CURDIR)/$@ $(notdir $(PAKDIR))

copy:
	@echo "===> COPY"
	@mkdir -p $(PAKDIR)/config
	@cp -p config/* $(PAKDIR)/config
	@mkdir -p $(PAKDIR)/text 
	@cp -p text/*.* $(PAKDIR)/text
#   @mkdir -p $(PAKDIR)/text/citylists 
	@mkdir -p $(PAKDIR)/sound
	@cp -p sound/* $(PAKDIR)/sound
	@python3 -m pak.fetch_wavs $(PAKDIR)/sound
#	@mkdir -p $(PAKDIR)/scenario
#	@cp -p scenario/* $(PAKDIR)/scenario
	@cp -p "$$(python3 -m pak.fetch_pak demo.sve)" $(PAKDIR)/demo.sve
	@cp -p licence.txt $(PAKDIR)
	@cp -p compat.tab $(PAKDIR)
	@cp -p "$$(python3 -m pak.fetch_pak symbol.BigLogo.pak)" $(PAKDIR)/symbol.BigLogo.pak

$(DIRS32):
	@echo "===> PAK32 $@"
	@mkdir -p $(PAKDIR)
	@$(MAKEOBJ) quiet PAK32 $(PAKDIR)/$(call make_name,$@) $(call ported_dats,$@) > /dev/null

$(DIRS64):
	@echo "===> PAK64 $@"
	@mkdir -p $(PAKDIR)
	@$(MAKEOBJ) quiet PAK $(PAKDIR)/$(call make_name,$@) $(call ported_dats,$@) > /dev/null

$(DIRS128):
	@echo "===> PAK128 $@"
	@mkdir -p $(PAKDIR)
	@$(MAKEOBJ) quiet PAK128 $(PAKDIR)/$(call make_name,$@) $(call ported_dats,$@) > /dev/null

$(DIRS192):
	@echo "===> PAK192 $@"
	@mkdir -p $(PAKDIR)
	@$(MAKEOBJ) quiet PAK192 $(PAKDIR)/$(call make_name,$@) $(call ported_dats,$@) > /dev/null

$(DIRS224):
	@echo "===> PAK224 $@"
	@mkdir -p $(PAKDIR)
	@$(MAKEOBJ) quiet PAK224 $(PAKDIR)/$(call make_name,$@) $(call ported_dats,$@) > /dev/null

$(DIRS256):
	@echo "===> PAK256 $@"
	@mkdir -p $(PAKDIR)
	@$(MAKEOBJ) quiet PAK256 $(PAKDIR)/$(call make_name,$@) $(call ported_dats,$@) > /dev/null

$(OUTSIDE):
	@echo "===> OUTSIDE with REVISION and grounds"
	@mkdir -p $(PAKDIR)
	@$(MAKEOBJ) quiet PAK128 $(PAKDIR)/ $(call ported_dats,$@) > /dev/null

# Parametric ground bakers under grounds/ — each <asset>.py emits
# <asset>.{png,dat} (back_wall emits both slopes and basement) and is
# self-contained.  Re-run the family with `make bake-grounds`; CI does
# not regenerate, the committed PNG/dat pairs are what ship.
GROUND_BAKERS := light_texture back_wall marker borders water \
                 shore_trans slope_trans sidewalk climate_texture

.PHONY: bake-grounds $(addprefix bake-,$(GROUND_BAKERS))

bake-grounds: $(addprefix bake-,$(GROUND_BAKERS))

$(addprefix bake-,$(GROUND_BAKERS)): bake-%:
	@echo "===> BAKE grounds/$*"
	@python3 -m grounds.$*

clean:
	@echo "===> CLEAN"
	@rm -fr $(PAKDIR) $(DESTFILE).tbz2 $(DESTFILE).zip simutranslator/*.zip

# -----------
# Everything after this point in the Makefile is designed for
# the generation of zip files to upload to simutranslator
# written by Nathanael Nerode
# -----------

# The following image files are too large for simutranslator.
OVERSIZE_IMAGES :=
OVERSIZE_IMAGES += attractions/images/cur/football-ground-lg.png
OVERSIZE_IMAGES += attractions/images/cur/cricket-ground-sm.png
OVERSIZE_IMAGES += boats/images/clan-line-steamer.png
OVERSIZE_IMAGES += boats/images/handysize.png


# For each zip file to generate,
# (1) Use 'find' to get everything under the directory;
# (2) But exclude everything in 'blends';
# (3) And only collect files with .dat and .png endings;
# (4) Then use zip, but exclude "known bad" image files.

simutranslator/%.zip:
	FILE_LIST=`find -path ./$*/\* \! -path ./$*/blends/\* \( -name \*.dat -o -name \*.png \)` ; \
	zip -r $@ $$FILE_LIST -x $(OVERSIZE_IMAGES)

# Special case: Program texts
simutranslator/program_texts.zip:
	zip $@ simutranslator/*.dat

# Convert the list of TR_DIRS to a list of TR_ZIPFILES
TR_ZIPFILES := $(patsubst %,simutranslator/%.zip, $(TR_DIRS) )

# Finally, depend on all the individual zipfiles.
simutranslator: $(TR_ZIPFILES)

# Potential problems.
# - The entire attractions folder may be too big to do in one go.
# - separate out the stone attractions?
STONE_ATTRACTIONS :=
STONE_ATTRACTIONS += attractions/stone-attractions.dat
STONE_ATTRACTIONS += attractions/images/cur/stone-attractions.png 
STONE_ATTRACTIONS += attractions/images/cur/stone-attractions-snow.png
# - The entire boats folder may also be too big
# - separate out the large boats?
# - The entire trains folder may ALSO be too big
