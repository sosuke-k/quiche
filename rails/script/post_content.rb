require "rubypython"

TAGS_TO_BE_REMOVED = [/<div>/, /<\/div>/, /\n/, /\t/, /<p>/, /<\/p>/].freeze

RubyPython.start

text = Item.all.first.content
TAGS_TO_BE_REMOVED.each { |pattern| text.gsub!(pattern, '') }
p text

dir = File.dirname __FILE__
sys = RubyPython.import 'sys'
sys.path.append File.join(dir, '.')
called_ruby = RubyPython.import("mecab_test")

called_ruby.func!( text: text ).rubify

RubyPython.stop
