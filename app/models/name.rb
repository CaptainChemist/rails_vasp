class Name < ActiveRecord::Base
  has_many :states
  has_many :coords
end
