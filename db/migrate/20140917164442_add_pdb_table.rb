class AddPdbTable < ActiveRecord::Migration
  def change
    create_table :coords do |t|
      t.integer :name_id
      t.string :atom
      t.string :atom_kind
      t.integer :atom_number


      t.timestamps

      end
    add_index :coords, :name_id
  end
end
