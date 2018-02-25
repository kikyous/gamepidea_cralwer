require './app'
# require 'minitest/autorun'
require 'rack/test'
require 'cgi'
require 'json'
require 'fileutils'
require 'eventmachine'

class ConcurrentRender
  # include Concurrent::Async

  def initialize(app)
    @app = app
  end

  def run(item)
    file = item.name
    res = MyRender.render @app, item
    dirname = File.dirname(file)
    unless File.directory?(dirname)
      FileUtils.mkdir_p("build/#{dirname}")
    end
    File.open("build/#{file}.html", 'w'){|f|f.write(res)}
  end
end
class Builder
  include Rack::Test::Methods

  def app
    Sinatra::Application
  end

  def index_json
    get '/index.json' do |res|
      File.open('build/index.json', 'w'){|f|f.write(res.body)}
    end
  end

  def build_page
    r = ConcurrentRender.new(Sinatra.new(Sinatra::Base).new!)
    Item.find_each do |i|
      r.run(i)
    end
  end

  def build_index
      get '/' do |res|
        File.open("build/index.html", 'w'){|f|f.write(res.body)}
      end
  end

  def copy_file
      FileUtils.cp_r('./public/.', './build/')
  end

  def run_all
      index_json
      build_page
      build_index
      copy_file
  end
end
Builder.new.run_all
# Builder.new.build_page
