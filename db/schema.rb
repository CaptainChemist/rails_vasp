# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20140814051849) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "names", force: true do |t|
    t.string   "calc_name"
    t.integer  "calc_num"
    t.string   "atom_list",    default: [], array: true
    t.string   "orbital_list", default: [], array: true
    t.string   "cluster_list", default: [], array: true
    t.boolean  "bound"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "states", force: true do |t|
    t.integer  "name_id"
    t.string   "energy_list",      default: [], array: true
    t.string   "dos_list",         default: [], array: true
    t.string   "atom_subset",      default: [], array: true
    t.integer  "orbital_subset"
    t.float    "fermi_level"
    t.float    "core_level"
    t.string   "elec_occ_list",    default: [], array: true
    t.string   "elec_energy_list", default: [], array: true
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "states", ["name_id"], name: "index_states_on_name_id", using: :btree

end
