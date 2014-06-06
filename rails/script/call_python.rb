require "rubypython"

RubyPython.start

# puts 'Pythonのクラスを呼び出す'
# cPickle = RubyPython.import("cPickle")
# p cPickle.dumps("Testing RubyPython.").rubify

# puts 'Pythonの自作メソッドを呼び出す'
dir = File.dirname __FILE__
sys = RubyPython.import 'sys'
sys.path.append File.join(dir, '.')
called_ruby = RubyPython.import("foo")
# called_ruby.print_python

# puts called_ruby.print_python_with_argument!( arg1: "Ruby String" ).rubify
# puts called_ruby.print_python_with_argument!( arg1: 1234 ).rubify
users = User.all
x = [0,1]
users.each do |user|
  x = called_ruby.func!( x: x ).rubify
  p x
end

RubyPython.stop
