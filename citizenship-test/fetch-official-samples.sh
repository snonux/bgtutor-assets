#!/bin/sh
# Downloads the official sample tests for the citizenship language exam into
# citizenship-test/official-samples/. Each file is taken from io.mon.bg first
# and from the bulgarian-citizenship.com mirror if that fails, and kept only if
# it really is a PDF. Run it from anywhere inside the repository.
set -u
cd "$(dirname "$0")" || exit 1
dir=official-samples
mkdir -p "$dir"
ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
mon=https://io.mon.bg/sites/default/files/uploads/docs/2013-06
mirror=https://www.bulgarian-citizenship.com/wp-content/uploads/2023/11

# fetch OUT URL... tries each URL in turn until one returns a PDF.
fetch() {
	out=$1
	shift
	for url in "$@"; do
		if curl -fsSL -A "$ua" -m 60 -o "$dir/$out" "$url" &&
			[ "$(head -c 4 "$dir/$out")" = "%PDF" ]; then
			echo "ok    $out  <- $url"
			return 0
		fi
		rm -f "$dir/$out"
	done
	echo "miss  $out"
	return 1
}

fetch variant_1.pdf "$mon/variant_1.pdf" "$mirror/Sample-Test-1.pdf"
fetch variant_2.pdf "$mon/variant_2.pdf" "$mirror/Sample-Test-2.pdf"
fetch variant_3.pdf "$mon/variant_3.pdf" "$mirror/Sample-Test-3.pdf"
# No further variants are known; these only probe in case MON adds some.
for n in 4 5 6; do
	fetch "variant_$n.pdf" "$mon/variant_$n.pdf" 2>/dev/null || true
done
ls -l "$dir"
