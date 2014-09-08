class CreateNames < ActiveRecord::Migration
  def change
    create_table :names do |t|
      t.string :calc_name
      t.integer :calc_num
      t.string   :atom_list,    default: [], array: true
      t.string   :orbital_list, default: [], array: true
      t.string   :cluster_list, default: [], array: true
      t.boolean  :bound
      t.timestamps
    end
  end
end
