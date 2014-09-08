class CreateStates < ActiveRecord::Migration
  def change
    create_table :states do |t|
      t.integer  :name_id
      t.string   :energy_list,      default: [], array: true
      t.string   :dos_list,         default: [], array: true
      t.string   :atom_subset,      default: [], array: true
      t.integer  :orbital_subset
      t.float    :fermi_level
      t.float    :core_level
      t.string   :elec_occ_list,    default: [], array: true
      t.string   :elec_energy_list, default: [], array: true

      t.timestamps
    end
    add_index :states, :name_id
  end
end
