require "rubypython"

TAGS_TO_BE_REMOVED = [/<div>/, /<\/div>/, /\n/, /\t/, /<p>/, /<\/p>/].freeze

CONTENT_FILE_NAME = "script/data_content.csv"
TAG_FILE_NAME = "script/data_tag.csv"

def write_content_and_tag item
	File.open(CONTENT_FILE_NAME, "a") { |file|
        content = item.content
        TAGS_TO_BE_REMOVED.each { |pattern| content.gsub!(pattern, '') }
	    content.gsub!(' ', '')
	    file.puts content
	}
	File.open(TAG_FILE_NAME, "a") { |file|
        tags = item.tag_list
        file.puts CSV.generate_line tags
	}
end

item = Item.first
write_content_and_tag item

RubyPython.start

items = Item.all
texts = []
for item in items
    text = item.content
    TAGS_TO_BE_REMOVED.each { |pattern| text.gsub!(pattern, '') }
    text.gsub!('、', '')
    text.gsub!('。', '')
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
