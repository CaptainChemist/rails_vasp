json.array!(@names) do |name|
  json.extract! name, :id, :calc_name
  json.url name_url(name, format: :json)
end
