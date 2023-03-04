# Japan Government Gender Breakdown

Quick project to determine the gender breakdown of the Japanese government (lower and upper houses).

`main.py` pulls images of elected officials from the most up-to-date sources:
* [https://www.shugiin.go.jp/internet/itdb_english.nsf/html/statics/member/mem_a.htm](https://www.shugiin.go.jp/internet/itdb_english.nsf/html/statics/member/mem_a.htm)
* [https://www.sangiin.go.jp/japanese/joho1/kousei/eng/members/index.htm](https://www.sangiin.go.jp/japanese/joho1/kousei/eng/members/index.htm)

`categorise.py` opens each image and allows the user to mark the gender using the left/right arrow keys. Gender is saved as a filename prefix.
