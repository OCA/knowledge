/* <pre><nowiki>
This is a copy of InstaView for use in other applications like [[User:Cacycle/wikEd|wikEd]].
 
Changes made:
	Fixed code duplication, fixed "doubled article name" bug in links. Cacycle 00:56, 9 September 2007 (UTC)
	The "Script to embed InstaView in MediaWiki's edit page" has been commented out
	added: // get values from MediaWiki global variables (Cacycle)
 
Installation:
	if (typeof(InstaView) != 'object')) {
		var script = document.createElement('script');
		script.type = 'text/javascript';
		script.src  = 'http://en.wikipedia.org/w/index.php?title=User:Pilaf/dev/instaview.js&action=raw&ctype=text/javascript&dontcountme=s';
		document.getElementsByTagName('head')[0].appendChild(script);
	}
 
*/
 
// Last update: Cacycle 22:26, 22 November 2008 (UTC)
 
/*
// Script to embed InstaView in MediaWiki's edit page
addOnloadHook(function(){
  if (document.getElementById('editpage-copywarn')) {
    var oldPreview = document.getElementById('wpPreview');
    var newPreview = document.createElement('input');
    newPreview.setAttribute('type', 'button');
    newPreview.setAttribute('style', 'font-style: italic');
    newPreview.setAttribute('value', 'InstaView');
    newPreview.setAttribute('id', 'InstaView');
    newPreview.setAttribute('name', 'InstaView');
    newPreview.setAttribute('onclick', "InstaView.dump('wpTextbox1', 'InstaViewDump')");
    oldPreview.parentNode.insertBefore(newPreview, oldPreview);
    oldPreview.parentNode.innerHTML += '<div style="margin: 5px 0 5px 0; padding: 5px; border: 2px solid orange;" id="InstaViewDump"></div>';
    oldPreview.value = 'Classic Preview';
    }
});
*/
 
/*
 * InstaView - a Mediawiki to HTML converter in JavaScript
 * Version 0.6.1
 * Copyright (C) Pedro Fayolle 2005-2006
 * http://en.wikipedia.org/wiki/User:Pilaf
 * Distributed under the BSD license
 *
 * Changelog:
 *
 * 0.6.1
 * - Fixed problem caused by \r characters
 * - Improved inline formatting parser
 *
 * 0.6
 * - Changed name to InstaView
 * - Some major code reorganizations and factored out some common functions
 * - Handled conversion of relative links (i.e. [[/foo]])
 * - Fixed misrendering of adjacent definition list items
 * - Fixed bug in table headings handling
 * - Changed date format in signatures to reflect Mediawiki's
 * - Fixed handling of [[:Image:...]]
 * - Updated MD5 function (hopefully it will work with UTF-8)
 * - Fixed bug in handling of links inside images
 *
 * To do:
 * - Better support for <math>
 * - Full support for <nowiki>
 * - Parser-based (as opposed to RegExp-based) inline wikicode handling (make it one-pass and bullet-proof)
 * - Support for templates (through AJAX)
 * - Support for coloured links (AJAX)
 */
 
 
var InstaView = {}
 
// options
InstaView.conf =
{
	user: {},
 
	wiki: {
		lang: 'en',
		interwiki: 'ab|aa|af|ak|sq|als|am|ang|ar|an|arc|hy|roa-rup|as|ast|av|ay|az|bm|ba|eu|be|bn|bh|bi|bs|br|bg|my|ca|ch|ce|chr|chy|ny|zh|zh-tw|zh-cn|cho|cv|kw|co|cr|hr|cs|da|dv|nl|dz|en|eo|et|ee|fo|fj|fi|fr|fy|ff|gl|ka|de|got|el|kl|gn|gu|ht|ha|haw|he|hz|hi|ho|hu|is|io|ig|id|ia|ie|iu|ik|ga|it|ja|jv|kn|kr|csb|ks|kk|km|ki|rw|rn|tlh|kv|kg|ko|kj|ku|ky|lo|la|lv|li|ln|lt|jbo|nds|lg|lb|mk|mg|ms|ml|mt|gv|mi|minnan|mr|mh|zh-min-nan|mo|mn|mus|nah|na|nv|ne|se|no|nn|oc|or|om|pi|fa|pl|pt|pa|ps|qu|ro|rm|ru|sm|sg|sa|sc|gd|sr|sh|st|tn|sn|scn|simple|sd|si|sk|sl|so|st|es|su|sw|ss|sv|tl|ty|tg|ta|tt|te|th|bo|ti|tpi|to|tokipona|ts|tum|tr|tk|tw|uk|ur|ug|uz|ve|vi|vo|wa|cy|wo|xh|ii|yi|yo|za|zu',
		default_thumb_width: 180
	},
 
	paths: {
		articles: '/wiki/',
		math: '/math/',
		images: '',
		images_fallback: 'http://upload.wikimedia.org/wikipedia/commons/',
		magnify_icon: 'skins/common/images/magnify-clip.png'
	},
 
	locale: {
		user: 'User',
		image: 'Image',
		category: 'Category',
		months: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	}
}
 
 
// get values from MediaWiki global variables (Cacycle)
if (typeof(wgArticlePath) != 'undefined') { InstaView.conf.paths.articles = wgArticlePath.replace(/\$1/, ''); }
if (typeof(wgContentLanguage) != 'undefined') { InstaView.conf.wiki.lang = wgContentLanguage; }
 
// options with default values or backreferences
with (InstaView.conf) {
	user.name = user.name || 'Wikipedian'
	user.signature = '[['+locale.user+':'+user.name+'|'+user.name+']]'
	paths.images = 'http://upload.wikimedia.org/wikipedia/' + wiki.lang + '/'
}
 
// define constants
InstaView.BLOCK_IMAGE = new RegExp('^\\[\\['+InstaView.conf.locale.image+':.*?\\|.*?(?:frame|thumbnail|thumb|none|right|left|center)', 'i');
 
InstaView.dump = function(from, to)
{
	if (typeof from == 'string') from = document.getElementById(from)
	if (typeof to == 'string') to = document.getElementById(to)
	to.innerHTML = this.convert(from.value)
}
 
InstaView.convert = function(wiki)
{
	var 	ll = (typeof wiki == 'string')? wiki.replace(/\r/g,'').split(/\n/): wiki, // lines of wikicode
		o='',	// output
		p=0,	// para flag
		$r	// result of passing a regexp to $()
 
	// some shorthands
	function remain() { return ll.length }
	function sh() { return ll.shift() } // shift
	function ps(s) { o+=s } // push
 
	function f() // similar to C's printf, uses ? as placeholders, ?? to escape question marks
	{
		var i=1,a=arguments,f=a[0],o='',c,p
		for (;i<a.length; i++) if ((p=f.indexOf('?'))+1) {
			// allow character escaping
			i -= c=f.charAt(p+1)=='?'?1:0
			o += f.substring(0,p)+(c?'?':a[i])
			f=f.substr(p+1+c)
		} else break;
		return o+f
	}
 
	function html_entities(s) { return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;") }
 
	function max(a,b) { return (a>b)?a:b }
	function min(a,b) { return (a<b)?a:b }
 
	// return the first non matching character position between two strings
	function str_imatch(a, b)
	{
		for (var i=0, l=min(a.length, b.length); i<l; i++) if (a.charAt(i)!=b.charAt(i)) break
		return i
	}
 
	// compare current line against a string or regexp
	// if passed a string it will compare only the first string.length characters
	// if passed a regexp the result is stored in $r
	function $(c) { return (typeof c == 'string') ? (ll[0].substr(0,c.length)==c) : ($r = ll[0].match(c)) }
 
	function $$(c) { return ll[0]==c } // compare current line against a string
	function _(p) { return ll[0].charAt(p) } // return char at pos p
 
	function endl(s) { ps(s); sh() }
 
	function parse_list()
	{
		var prev='';
 
		while (remain() && $(/^([*#:;]+)(.*)$/)) {
 
			var l_match = $r
 
			sh()
 
			var ipos = str_imatch(prev, l_match[1])
 
			// close uncontinued lists
			for (var i=prev.length-1; i >= ipos; i--) {
 
				var pi = prev.charAt(i)
 
				if (pi=='*') ps('</ul>')
				else if (pi=='#') ps('</ol>')
				// close a dl only if the new item is not a dl item (:, ; or empty)
				else switch (l_match[1].charAt(i)) { case'':case'*':case'#': ps('</dl>') }
			}
 
			// open new lists
			for (var i=ipos; i<l_match[1].length; i++) {
 
				var li = l_match[1].charAt(i)
 
				if (li=='*') ps('<ul>')
				else if (li=='#') ps('<ol>')
				// open a new dl only if the prev item is not a dl item (:, ; or empty)
				else switch(prev.charAt(i)) { case'':case'*':case'#': ps('<dl>') }
			}
 
			switch (l_match[1].charAt(l_match[1].length-1)) {
 
				case '*': case '#':
					ps('<li>' + parse_inline_nowiki(l_match[2])); break
 
				case ';':
					ps('<dt>')
 
					var dt_match
 
					// handle ;dt :dd format
					if (dt_match = l_match[2].match(/(.*?) (:.*?)$/)) {
 
						ps(parse_inline_nowiki(dt_match[1]))
						ll.unshift(dt_match[2])
 
					} else ps(parse_inline_nowiki(l_match[2]))
 
					break
 
				case ':':
					ps('<dd>' + parse_inline_nowiki(l_match[2]))
			}
 
			prev=l_match[1]
		}
 
		// close remaining lists
		for (var i=prev.length-1; i>=0; i--)
			ps(f('</?>', (prev.charAt(i)=='*')? 'ul': ((prev.charAt(i)=='#')? 'ol': 'dl')))
	}
 
	function parse_table()
	{
		endl(f('<table?>', $(/^\{\|( .*)$/)? $r[1]: ''))
 
		for (;remain();) if ($('|')) switch (_(1)) {
			case '}': endl('</table>'); return
			case '-': endl(f('<tr ?>', $(/\|-*(.*)/)[1])); break
			default: parse_table_data()
		}
		else if ($('!')) parse_table_data()
		else sh()
	}
 
	function parse_table_data()
	{
		var td_line, match_i
 
		// 1: "|+", '|' or '+'
		// 2: ??
		// 3: attributes ??
		// TODO: finish commenting this regexp
		var td_match = sh().match(/^(\|\+|\||!)((?:([^[|]*?)\|(?!\|))?(.*))$/)
 
		if (td_match[1] == '|+') ps('<caption');
		else ps('<t' + ((td_match[1]=='|')?'d':'h'))
 
		if (typeof td_match[3] != 'undefined') {
 
			ps(' ' + td_match[3])
			match_i = 4
 
		} else match_i = 2
 
		ps('>')
 
		if (td_match[1] != '|+') {
 
			// use || or !! as a cell separator depending on context
			// NOTE: when split() is passed a regexp make sure to use non-capturing brackets
			td_line = td_match[match_i].split((td_match[1] == '|')? '||': /(?:\|\||!!)/)
 
			ps(parse_inline_nowiki(td_line.shift()))
 
			while (td_line.length) ll.unshift(td_match[1] + td_line.pop())
 
		} else ps(td_match[match_i])
 
		var tc = 0, td = []
 
		for (;remain(); td.push(sh()))
		if ($('|')) {
			if (!tc) break // we're at the outer-most level (no nested tables), skip to td parse
			else if (_(1)=='}') tc--
		}
		else if (!tc && $('!')) break
		else if ($('{|')) tc++
 
		if (td.length) ps(InstaView.convert(td))
	}
 
	function parse_pre()
	{
		ps('<pre>')
		do endl(parse_inline_nowiki(ll[0].substring(1)) + "\n"); while (remain() && $(' '))
		ps('</pre>')
	}
 
	function parse_block_image()
	{
		ps(parse_image(sh()))
	}
 
	function parse_image(str)
	{
		// get what's in between "[[Image:" and "]]"
		var tag = str.substring(InstaView.conf.locale.image.length + 3, str.length - 2);
 
		var width;
		var attr = [], filename, caption = '';
		var thumb=0, frame=0, center=0;
		var align='';
 
		if (tag.match(/\|/)) {
			// manage nested links
			var nesting = 0;
			var last_attr;
			for (var i = tag.length-1; i > 0; i--) {
				if (tag.charAt(i) == '|' && !nesting) {
					last_attr = tag.substr(i+1);
					tag = tag.substring(0, i);
					break;
				} else switch (tag.substr(i-1, 2)) {
					case ']]':
						nesting++;
						i--;
						break;
					case '[[':
						nesting--;
						i--;
				}
			}
 
			attr = tag.split(/\s*\|\s*/);
			attr.push(last_attr);
			filename = attr.shift();
 
			var w_match;
 
			for (;attr.length; attr.shift())
			if (w_match = attr[0].match(/^(\d*)px$/)) width = w_match[1]
			else switch(attr[0]) {
				case 'thumb':
				case 'thumbnail':
					thumb=true;
				case 'frame':
					frame=true;
					break;
				case 'none':
				case 'right':
				case 'left':
					center=false;
					align=attr[0];
					break;
				case 'center':
					center=true;
					align='none';
					break;
				default:
					if (attr.length == 1) caption = attr[0];
			}
 
		} else filename = tag;
 
 
		var o='';
 
		if (frame) {
 
			if (align=='') align = 'right';
 
			o += f("<div class='thumb t?'>", align);
 
			if (thumb) {
				if (!width) width = InstaView.conf.wiki.default_thumb_width;
 
				o += f("<div style='width:?px;'>?", 2+width*1, make_image(filename, caption, width)) +
					f("<div class='thumbcaption'><div class='magnify' style='float:right'><a href='?' class='internal' title='Enlarge'><img src='?'></a></div>?</div>",
						InstaView.conf.paths.articles + InstaView.conf.locale.image + ':' + filename,
						InstaView.conf.paths.magnify_icon,
						parse_inline_nowiki(caption)
					)
			} else {
				o += '<div>' + make_image(filename, caption) + f("<div class='thumbcaption'>?</div>", parse_inline_nowiki(caption))
			}
 
			o += '</div></div>';
 
		} else if (align != '') {
			o += f("<div class='float?'><span>?</span></div>", align, make_image(filename, caption, width));
		} else {
			return make_image(filename, caption, width);
		}
 
		return center? f("<div class='center'>?</div>", o): o;
	}
 
	function parse_inline_nowiki(str)
	{
		var start, lastend=0
		var substart=0, nestlev=0, open, close, subloop;
		var html='';
 
		while (-1 != (start = str.indexOf('<nowiki>', substart))) {
			html += parse_inline_wiki(str.substring(lastend, start));
			start += 8;
			substart = start;
			subloop = true;
			do {
				open = str.indexOf('<nowiki>', substart);
				close = str.indexOf('</nowiki>', substart);
				if (close<=open || open==-1) {
					if (close==-1) {
						return html + html_entities(str.substr(start));
					}
					substart = close+9;
					if (nestlev) {
						nestlev--;
					} else {
						lastend = substart;
						html += html_entities(str.substring(start, lastend-9));
						subloop = false;
					}
				} else {
					substart = open+8;
					nestlev++;
				}
			} while (subloop)
		}
 
		return html + parse_inline_wiki(str.substr(lastend));
	}
 
	function make_image(filename, caption, width)
	{
		// uppercase first letter in file name
		filename = filename.charAt(0).toUpperCase() + filename.substr(1);
		// replace spaces with underscores
		filename = filename.replace(/ /g, '_');
 
		caption = strip_inline_wiki(caption);
 
		var md5 = hex_md5(filename);
 
		var source = md5.charAt(0) + '/' + md5.substr(0,2) + '/' + filename;
 
		if (width) width = "width='" + width + "px'";
 
		var img = f("<img onerror=\"this.onerror=null;this.src='?'\" src='?' ? ?>", InstaView.conf.paths.images_fallback + source, InstaView.conf.paths.images + source, (caption!='')? "alt='" + caption + "'" : '', width);
 
		return f("<a class='image' ? href='?'>?</a>", (caption!='')? "title='" + caption + "'" : '', InstaView.conf.paths.articles + InstaView.conf.locale.image + ':' + filename, img);
	}
 
	function parse_inline_images(str)
	{
		var start, substart=0, nestlev=0;
		var loop, close, open, wiki, html;
 
		while (-1 != (start=str.indexOf('[[', substart))) {
			if(str.substr(start+2).match(RegExp('^' + InstaView.conf.locale.image + ':','i'))) {
				loop=true;
				substart=start;
				do {
					substart+=2;
					close=str.indexOf(']]',substart);
					open=str.indexOf('[[',substart);
					if (close<=open||open==-1) {
						if (close==-1) return str;
						substart=close;
						if (nestlev) {
							nestlev--;
						} else {
							wiki=str.substring(start,close+2);
							html=parse_image(wiki);
							str=str.replace(wiki,html);
							substart=start+html.length;
							loop=false;
						}
					} else {
						substart=open;
						nestlev++;
					}
				} while (loop)
 
			} else break;
		}
 
		return str;
	}
 
	// the output of this function doesn't respect the FILO structure of HTML
	// but since most browsers can handle it I'll save myself the hassle
	function parse_inline_formatting(str)
	{
		var em,st,i,li,o='';
		while ((i=str.indexOf("''",li))+1) {
			o += str.substring(li,i);
			li=i+2;
			if (str.charAt(i+2)=="'") {
				li++;
				st=!st;
				o+=st?'<strong>':'</strong>';
			} else {
				em=!em;
				o+=em?'<em>':'</em>';
			}
		}
		return o+str.substr(li);
	}
 
	function parse_inline_wiki(str)
	{
		var aux_match;
 
		str = parse_inline_images(str);
		str = parse_inline_formatting(str);
 
		// math
		while (aux_match = str.match(/<(?:)math>(.*?)<\/math>/i)) {
			var math_md5 = hex_md5(aux_match[1]);
			str = str.replace(aux_match[0], f("<img src='?.png'>", InstaView.conf.paths.math+math_md5));
		}
 
		// Build a Mediawiki-formatted date string
		var date = new Date;
		var minutes = date.getUTCMinutes();
		if (minutes < 10) minutes = '0' + minutes;
		var date = f("?:?, ? ? ? (UTC)", date.getUTCHours(), minutes, date.getUTCDate(), InstaView.conf.locale.months[date.getUTCMonth()], date.getUTCFullYear());
 
		// text formatting
		return str.
			// signatures
			replace(/~{5}(?!~)/g, date).
			replace(/~{4}(?!~)/g, InstaView.conf.user.name+' '+date).
			replace(/~{3}(?!~)/g, InstaView.conf.user.name).
 
			// [[:Category:...]], [[:Image:...]], etc...
			replace(RegExp('\\[\\[:((?:'+InstaView.conf.locale.category+'|'+InstaView.conf.locale.image+'|'+InstaView.conf.wiki.interwiki+'):.*?)\\]\\]','gi'), "<a href='"+InstaView.conf.paths.articles+"$1'>$1</a>").
			replace(RegExp('\\[\\[(?:'+InstaView.conf.locale.category+'|'+InstaView.conf.wiki.interwiki+'):.*?\\]\\]','gi'),'').
 
			// [[/Relative links]]
			replace(/\[\[(\/[^|]*?)\]\]/g, f("<a href='?$1'>$1</a>", location)).
 
			// [[/Replaced|Relative links]]
			replace(/\[\[(\/.*?)\|(.+?)\]\]/g, f("<a href='?$1'>$2</a>", location)).
 
			// [[Common links]]
			replace(/\[\[([^|]*?)\]\](\w*)/g, f("<a href='?$1'>$1$2</a>", InstaView.conf.paths.articles)).
 
			// [[Replaced|Links]]
			replace(/\[\[(.*?)\|([^\]]+?)\]\](\w*)/g, f("<a href='?$1'>$2$3</a>", InstaView.conf.paths.articles)).
 
			// [[Stripped:Namespace|Namespace]]
			replace(/\[\[([^\]]*?:)?(.*?)( *\(.*?\))?\|\]\]/g, f("<a href='?$1$2$3'>$2</a>", InstaView.conf.paths.articles)).
 
			// External links
			replace(/\[(https?|news|ftp|mailto|gopher|irc):(\/*)([^\]]*?) (.*?)\]/g, "<a href='$1:$2$3'>$4</a>").
			replace(/\[http:\/\/(.*?)\]/g, "<a href='http://$1'>[#]</a>").
			replace(/\[(news|ftp|mailto|gopher|irc):(\/*)(.*?)\]/g, "<a href='$1:$2$3'>$1:$2$3</a>").
			replace(/(^| )(https?|news|ftp|mailto|gopher|irc):(\/*)([^ $]*)/g, "$1<a href='$2:$3$4'>$2:$3$4</a>").
 
			replace('__NOTOC__','').
			replace('__NOEDITSECTION__','');
	}
 
	function strip_inline_wiki(str)
	{
		return str
			.replace(/\[\[[^\]]*\|(.*?)\]\]/g,'$1')
			.replace(/\[\[(.*?)\]\]/g,'$1')
			.replace(/''(.*?)''/g,'$1');
	}
 
	// begin parsing
	for (;remain();) if ($(/^(={1,6})(.*)\1(.*)$/)) {
		p=0
		endl(f('<h?>?</h?>?', $r[1].length, parse_inline_nowiki($r[2]), $r[1].length, $r[3]))
 
	} else if ($(/^[*#:;]/)) {
		p=0
		parse_list()
 
	} else if ($(' ')) {
		p=0
		parse_pre()
 
	} else if ($('{|')) {
		p=0
		parse_table()
 
	} else if ($(/^----+$/)) {
		p=0
		endl('<hr>')
 
	} else if ($(InstaView.BLOCK_IMAGE)) {
		p=0
		parse_block_image()
 
	} else {
 
		// handle paragraphs
		if ($$('')) {
			if (p = (remain()>1 && ll[1]==(''))) endl('<p><br>')
		} else {
			if(!p) {
				ps('<p>')
				p=1
			}
			ps(parse_inline_nowiki(ll[0]) + ' ')
		}
 
		sh();
	}
 
	return o
}
 
 
/*
 * A JavaScript implementation of the RSA Data Security, Inc. MD5 Message
 * Digest Algorithm, as defined in RFC 1321.
 * Version 2.2-alpha Copyright (C) Paul Johnston 1999 - 2005
 * Other contributors: Greg Holt, Andrew Kepert, Ydnar, Lostinet
 * Distributed under the BSD License
 * See http://pajhome.org.uk/crypt/md5 for more info.
 */
 
/*
 * Configurable variables. You may need to tweak these to be compatible with
 * the server-side, but the defaults work in most cases.
 */
var hexcase = 0;   /* hex output format. 0 - lowercase; 1 - uppercase        */
var b64pad  = ""; /* base-64 pad character. "=" for strict RFC compliance   */
 
/*
 * These are the functions you'll usually want to call
 * They take string arguments and return either hex or base-64 encoded strings
 */
function hex_md5(s)    { return rstr2hex(rstr_md5(str2rstr_utf8(s))); }
function b64_md5(s)    { return rstr2b64(rstr_md5(str2rstr_utf8(s))); }
function any_md5(s, e) { return rstr2any(rstr_md5(str2rstr_utf8(s)), e); }
function hex_hmac_md5(k, d)
  { return rstr2hex(rstr_hmac_md5(str2rstr_utf8(k), str2rstr_utf8(d))); }
function b64_hmac_md5(k, d)
  { return rstr2b64(rstr_hmac_md5(str2rstr_utf8(k), str2rstr_utf8(d))); }
function any_hmac_md5(k, d, e)
  { return rstr2any(rstr_hmac_md5(str2rstr_utf8(k), str2rstr_utf8(d)), e); }
 
/*
 * Calculate the MD5 of a raw string
 */
function rstr_md5(s)
{
  return binl2rstr(binl_md5(rstr2binl(s), s.length * 8));
}
 
/*
 * Calculate the HMAC-MD5, of a key and some data (raw strings)
 */
function rstr_hmac_md5(key, data)
{
  var bkey = rstr2binl(key);
  if(bkey.length > 16) bkey = binl_md5(bkey, key.length * 8);
 
  var ipad = Array(16), opad = Array(16);
  for(var i = 0; i < 16; i++)
  {
    ipad[i] = bkey[i] ^ 0x36363636;
    opad[i] = bkey[i] ^ 0x5C5C5C5C;
  }
 
  var hash = binl_md5(ipad.concat(rstr2binl(data)), 512 + data.length * 8);
  return binl2rstr(binl_md5(opad.concat(hash), 512 + 128));
}
 
/*
 * Convert a raw string to a hex string
 */
function rstr2hex(input)
{
  var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
  var output = "";
  var x;
  for(var i = 0; i < input.length; i++)
  {
    x = input.charCodeAt(i);
    output += hex_tab.charAt((x >>> 4) & 0x0F)
           +  hex_tab.charAt( x        & 0x0F);
  }
  return output;
}
 
/*
 * Convert a raw string to a base-64 string
 */
function rstr2b64(input)
{
  var tab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  var output = "";
  var len = input.length;
  for(var i = 0; i < len; i += 3)
  {
    var triplet = (input.charCodeAt(i) << 16)
                | (i + 1 < len ? input.charCodeAt(i+1) << 8 : 0)
                | (i + 2 < len ? input.charCodeAt(i+2)      : 0);
    for(var j = 0; j < 4; j++)
    {
      if(i * 8 + j * 6 > input.length * 8) output += b64pad;
      else output += tab.charAt((triplet >>> 6*(3-j)) & 0x3F);
    }
  }
  return output;
}
 
/*
 * Convert a raw string to an arbitrary string encoding
 */
function rstr2any(input, encoding)
{
  var divisor = encoding.length;
  var remainders = Array();
  var i, q, x, quotient;
 
  /* Convert to an array of 16-bit big-endian values, forming the dividend */
  var dividend = Array(input.length / 2);
  for(i = 0; i < dividend.length; i++)
  {
    dividend[i] = (input.charCodeAt(i * 2) << 8) | input.charCodeAt(i * 2 + 1);
  }
 
  /*
   * Repeatedly perform a long division. The binary array forms the dividend,
   * the length of the encoding is the divisor. Once computed, the quotient
   * forms the dividend for the next step. We stop when the dividend is zero.
   * All remainders are stored for later use.
   */
  while(dividend.length > 0)
  {
    quotient = Array();
    x = 0;
    for(i = 0; i < dividend.length; i++)
    {
      x = (x << 16) + dividend[i];
      q = Math.floor(x / divisor);
      x -= q * divisor;
      if(quotient.length > 0 || q > 0)
        quotient[quotient.length] = q;
    }
    remainders[remainders.length] = x;
    dividend = quotient;
  }
 
  /* Convert the remainders to the output string */
  var output = "";
  for(i = remainders.length - 1; i >= 0; i--)
    output += encoding.charAt(remainders[i]);
 
  return output;
}
 
/*
 * Encode a string as utf-8.
 * For efficiency, this assumes the input is valid utf-16.
 */
function str2rstr_utf8(input)
{
  var output = "";
  var i = -1;
  var x, y;
 
  while(++i < input.length)
  {
    /* Decode utf-16 surrogate pairs */
    x = input.charCodeAt(i);
    y = i + 1 < input.length ? input.charCodeAt(i + 1) : 0;
    if(0xD800 <= x && x <= 0xDBFF && 0xDC00 <= y && y <= 0xDFFF)
    {
      x = 0x10000 + ((x & 0x03FF) << 10) + (y & 0x03FF);
      i++;
    }
 
    /* Encode output as utf-8 */
    if(x <= 0x7F)
      output += String.fromCharCode(x);
    else if(x <= 0x7FF)
      output += String.fromCharCode(0xC0 | ((x >>> 6 ) & 0x1F),
                                    0x80 | ( x         & 0x3F));
    else if(x <= 0xFFFF)
      output += String.fromCharCode(0xE0 | ((x >>> 12) & 0x0F),
                                    0x80 | ((x >>> 6 ) & 0x3F),
                                    0x80 | ( x         & 0x3F));
    else if(x <= 0x1FFFFF)
      output += String.fromCharCode(0xF0 | ((x >>> 18) & 0x07),
                                    0x80 | ((x >>> 12) & 0x3F),
                                    0x80 | ((x >>> 6 ) & 0x3F),
                                    0x80 | ( x         & 0x3F));
  }
  return output;
}
 
/*
 * Encode a string as utf-16
 */
function str2rstr_utf16le(input)
{
  var output = "";
  for(var i = 0; i < input.length; i++)
    output += String.fromCharCode( input.charCodeAt(i)        & 0xFF,
                                  (input.charCodeAt(i) >>> 8) & 0xFF);
  return output;
}
 
function str2rstr_utf16be(input)
{
  var output = "";
  for(var i = 0; i < input.length; i++)
    output += String.fromCharCode((input.charCodeAt(i) >>> 8) & 0xFF,
                                   input.charCodeAt(i)        & 0xFF);
  return output;
}
 
/*
 * Convert a raw string to an array of little-endian words
 * Characters >255 have their high-byte silently ignored.
 */
function rstr2binl(input)
{
  var output = Array(input.length >> 2);
  for(var i = 0; i < output.length; i++)
    output[i] = 0;
  for(var i = 0; i < input.length * 8; i += 8)
    output[i>>5] |= (input.charCodeAt(i / 8) & 0xFF) << (i%32);
  return output;
}
 
/*
 * Convert an array of little-endian words to a string
 */
function binl2rstr(input)
{
  var output = "";
  for(var i = 0; i < input.length * 32; i += 8)
    output += String.fromCharCode((input[i>>5] >>> (i % 32)) & 0xFF);
  return output;
}
 
/*
 * Calculate the MD5 of an array of little-endian words, and a bit length.
 */
function binl_md5(x, len)
{
  /* append padding */
  x[len >> 5] |= 0x80 << ((len) % 32);
  x[(((len + 64) >>> 9) << 4) + 14] = len;
 
  var a =  1732584193;
  var b = -271733879;
  var c = -1732584194;
  var d =  271733878;
 
  for(var i = 0; i < x.length; i += 16)
  {
    var olda = a;
    var oldb = b;
    var oldc = c;
    var oldd = d;
 
    a = md5_ff(a, b, c, d, x[i+ 0], 7 , -680876936);
    d = md5_ff(d, a, b, c, x[i+ 1], 12, -389564586);
    c = md5_ff(c, d, a, b, x[i+ 2], 17,  606105819);
    b = md5_ff(b, c, d, a, x[i+ 3], 22, -1044525330);
    a = md5_ff(a, b, c, d, x[i+ 4], 7 , -176418897);
    d = md5_ff(d, a, b, c, x[i+ 5], 12,  1200080426);
    c = md5_ff(c, d, a, b, x[i+ 6], 17, -1473231341);
    b = md5_ff(b, c, d, a, x[i+ 7], 22, -45705983);
    a = md5_ff(a, b, c, d, x[i+ 8], 7 ,  1770035416);
    d = md5_ff(d, a, b, c, x[i+ 9], 12, -1958414417);
    c = md5_ff(c, d, a, b, x[i+10], 17, -42063);
    b = md5_ff(b, c, d, a, x[i+11], 22, -1990404162);
    a = md5_ff(a, b, c, d, x[i+12], 7 ,  1804603682);
    d = md5_ff(d, a, b, c, x[i+13], 12, -40341101);
    c = md5_ff(c, d, a, b, x[i+14], 17, -1502002290);
    b = md5_ff(b, c, d, a, x[i+15], 22,  1236535329);
 
    a = md5_gg(a, b, c, d, x[i+ 1], 5 , -165796510);
    d = md5_gg(d, a, b, c, x[i+ 6], 9 , -1069501632);
    c = md5_gg(c, d, a, b, x[i+11], 14,  643717713);
    b = md5_gg(b, c, d, a, x[i+ 0], 20, -373897302);
    a = md5_gg(a, b, c, d, x[i+ 5], 5 , -701558691);
    d = md5_gg(d, a, b, c, x[i+10], 9 ,  38016083);
    c = md5_gg(c, d, a, b, x[i+15], 14, -660478335);
    b = md5_gg(b, c, d, a, x[i+ 4], 20, -405537848);
    a = md5_gg(a, b, c, d, x[i+ 9], 5 ,  568446438);
    d = md5_gg(d, a, b, c, x[i+14], 9 , -1019803690);
    c = md5_gg(c, d, a, b, x[i+ 3], 14, -187363961);
    b = md5_gg(b, c, d, a, x[i+ 8], 20,  1163531501);
    a = md5_gg(a, b, c, d, x[i+13], 5 , -1444681467);
    d = md5_gg(d, a, b, c, x[i+ 2], 9 , -51403784);
    c = md5_gg(c, d, a, b, x[i+ 7], 14,  1735328473);
    b = md5_gg(b, c, d, a, x[i+12], 20, -1926607734);
 
    a = md5_hh(a, b, c, d, x[i+ 5], 4 , -378558);
    d = md5_hh(d, a, b, c, x[i+ 8], 11, -2022574463);
    c = md5_hh(c, d, a, b, x[i+11], 16,  1839030562);
    b = md5_hh(b, c, d, a, x[i+14], 23, -35309556);
    a = md5_hh(a, b, c, d, x[i+ 1], 4 , -1530992060);
    d = md5_hh(d, a, b, c, x[i+ 4], 11,  1272893353);
    c = md5_hh(c, d, a, b, x[i+ 7], 16, -155497632);
    b = md5_hh(b, c, d, a, x[i+10], 23, -1094730640);
    a = md5_hh(a, b, c, d, x[i+13], 4 ,  681279174);
    d = md5_hh(d, a, b, c, x[i+ 0], 11, -358537222);
    c = md5_hh(c, d, a, b, x[i+ 3], 16, -722521979);
    b = md5_hh(b, c, d, a, x[i+ 6], 23,  76029189);
    a = md5_hh(a, b, c, d, x[i+ 9], 4 , -640364487);
    d = md5_hh(d, a, b, c, x[i+12], 11, -421815835);
    c = md5_hh(c, d, a, b, x[i+15], 16,  530742520);
    b = md5_hh(b, c, d, a, x[i+ 2], 23, -995338651);
 
    a = md5_ii(a, b, c, d, x[i+ 0], 6 , -198630844);
    d = md5_ii(d, a, b, c, x[i+ 7], 10,  1126891415);
    c = md5_ii(c, d, a, b, x[i+14], 15, -1416354905);
    b = md5_ii(b, c, d, a, x[i+ 5], 21, -57434055);
    a = md5_ii(a, b, c, d, x[i+12], 6 ,  1700485571);
    d = md5_ii(d, a, b, c, x[i+ 3], 10, -1894986606);
    c = md5_ii(c, d, a, b, x[i+10], 15, -1051523);
    b = md5_ii(b, c, d, a, x[i+ 1], 21, -2054922799);
    a = md5_ii(a, b, c, d, x[i+ 8], 6 ,  1873313359);
    d = md5_ii(d, a, b, c, x[i+15], 10, -30611744);
    c = md5_ii(c, d, a, b, x[i+ 6], 15, -1560198380);
    b = md5_ii(b, c, d, a, x[i+13], 21,  1309151649);
    a = md5_ii(a, b, c, d, x[i+ 4], 6 , -145523070);
    d = md5_ii(d, a, b, c, x[i+11], 10, -1120210379);
    c = md5_ii(c, d, a, b, x[i+ 2], 15,  718787259);
    b = md5_ii(b, c, d, a, x[i+ 9], 21, -343485551);
 
    a = safe_add(a, olda);
    b = safe_add(b, oldb);
    c = safe_add(c, oldc);
    d = safe_add(d, oldd);
  }
  return Array(a, b, c, d);
}
 
/*
 * These functions implement the four basic operations the algorithm uses.
 */
function md5_cmn(q, a, b, x, s, t)
{
  return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s),b);
}
function md5_ff(a, b, c, d, x, s, t)
{
  return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t);
}
function md5_gg(a, b, c, d, x, s, t)
{
  return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t);
}
function md5_hh(a, b, c, d, x, s, t)
{
  return md5_cmn(b ^ c ^ d, a, b, x, s, t);
}
function md5_ii(a, b, c, d, x, s, t)
{
  return md5_cmn(c ^ (b | (~d)), a, b, x, s, t);
}
 
/*
 * Add integers, wrapping at 2^32. This uses 16-bit operations internally
 * to work around bugs in some JS interpreters.
 */
function safe_add(x, y)
{
  var lsw = (x & 0xFFFF) + (y & 0xFFFF);
  var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
  return (msw << 16) | (lsw & 0xFFFF);
}
 
/*
 * Bitwise rotate a 32-bit number to the left.
 */
function bit_rol(num, cnt)
{
  return (num << cnt) | (num >>> (32 - cnt));
}