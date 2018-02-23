require 'sinatra'
require "sinatra/json"
require 'sinatra/activerecord'

require "sinatra/reloader" if development?
require 'cgi'
require 'json'
require 'nokogiri'
require 'pry'


set :database, "sqlite3:example.db"
class Item < ActiveRecord::Base
  def en
    name = en_name.split('gamepedia.com/')[1] if en_name
    CGI.unescape(name).gsub('_', ' ') if name
  end
end

def htmlpipe(html)
  doc = Nokogiri::HTML.fragment(html)
  doc.xpath('.//comment()').remove
  %w(.printfooter .catlinks #siteSub #jump-to-nav .mw-editsection #contentSub).each do |i|
    doc.css(i).remove
  end
  doc.to_s
end


get '/index.json' do
    result = Item.all.sort_by{|i|i.name.length}.map{|i| {cn: i.name, en: i.en}  }
  p result.size
  json( { data: result })
end

get '/' do
  name = 'index'
  erb :layout, layout: false, locals: { item: nil } do
    htmlpipe(File.read "#{name}.html")
  end
end

def _render(item)
end

get '/*' do
  name = params['splat'].first.split('.html').first
  name = CGI.unescape(name)
  item = Item.find_by(name: name)
  MyRender.render(self, item)
end

post 'build_all' do
  runner = ConcurrentRender.new
  Item.all.each do |i|
    runner.async.render(i)
  end
end

class MyRender
  def self.render(context, item)
    context.erb :layout, layout: false, locals: { item: item } do
      htmlpipe(item.content)
    end
  end
end

# i = Item.find_by(name: '盔甲')
# c = ConcurrentRender.new
#
