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

ActiveRecord::Schema.define(version: 20170522192527) do

  create_table "bookmakers_caches", force: :cascade do |t|
    t.integer  "first_id"
    t.integer  "second_id"
    t.string   "result"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["first_id"], name: "index_bookmakers_caches_on_first_id"
    t.index ["second_id"], name: "index_bookmakers_caches_on_second_id"
  end

  create_table "individual_features_caches", force: :cascade do |t|
    t.integer  "first_id"
    t.integer  "second_id"
    t.string   "result"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["first_id"], name: "index_individual_features_caches_on_first_id"
    t.index ["second_id"], name: "index_individual_features_caches_on_second_id"
  end

  create_table "libraries", force: :cascade do |t|
    t.string   "title"
    t.string   "author"
    t.date     "date_published"
    t.datetime "created_at",     null: false
    t.datetime "updated_at",     null: false
  end

  create_table "pair_features_caches", force: :cascade do |t|
    t.integer  "first_id"
    t.integer  "second_id"
    t.string   "result"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["first_id"], name: "index_pair_features_caches_on_first_id"
    t.index ["second_id"], name: "index_pair_features_caches_on_second_id"
  end

  create_table "players", force: :cascade do |t|
    t.integer  "oncourt_id"
    t.string   "name"
    t.date     "birthdate"
    t.string   "country"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer  "rank"
    t.integer  "prize"
    t.index ["name"], name: "index_players_on_name"
    t.index ["oncourt_id"], name: "index_players_on_oncourt_id", unique: true
    t.index ["prize"], name: "index_players_on_prize"
    t.index ["rank"], name: "index_players_on_rank"
  end

  create_table "predict_caches", force: :cascade do |t|
    t.integer  "first_id"
    t.integer  "second_id"
    t.string   "result"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["first_id"], name: "index_predict_caches_on_first_id"
    t.index ["second_id"], name: "index_predict_caches_on_second_id"
  end

  create_table "strength_triangle_caches", force: :cascade do |t|
    t.integer  "first_id"
    t.integer  "second_id"
    t.string   "result"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["first_id"], name: "index_strength_triangle_caches_on_first_id"
    t.index ["second_id"], name: "index_strength_triangle_caches_on_second_id"
  end

end
