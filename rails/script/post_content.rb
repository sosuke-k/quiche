require "rubypython"

TAGS_TO_BE_REMOVED = [/<div>/, /<\/div>/, /\n/, /\t/, /<p>/, /<\/p>/].freeze

RubyPython.start

items = Item.all
texts = []
for item in items
    text = item.content
    TAGS_TO_BE_REMOVED.each { |pattern| text.gsub!(pattern, '') }
    text.gsub!('、', '')
    text.gsub!('。', '')
    text.gsub!(' ', '')
    texts << text
end
# p text

dir = File.dirname __FILE__
sys = RubyPython.import 'sys'
sys.path.append File.join(dir, '.')
called_ruby = RubyPython.import("mecab_test")

x = called_ruby.func!( texts: texts ).rubify

# puts x

RubyPython.stop

# p text
