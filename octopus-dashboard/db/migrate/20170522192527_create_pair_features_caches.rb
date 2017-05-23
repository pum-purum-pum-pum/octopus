class CreatePairFeaturesCaches < ActiveRecord::Migration[5.0]
  def change
    create_table :pair_features_caches do |t|
      t.integer :first_id
      t.integer :second_id
      t.string :result

      t.timestamps
    end
    add_index :pair_features_caches, :first_id
    add_index :pair_features_caches, :second_id

    create_table :bookmakers_caches do |t|
      t.integer :first_id
      t.integer :second_id
      t.string :result

      t.timestamps
    end
    add_index :bookmakers_caches, :first_id
    add_index :bookmakers_caches, :second_id

    create_table :strength_triangle_caches do |t|
      t.integer :first_id
      t.integer :second_id
      t.string :result

      t.timestamps
    end
    add_index :strength_triangle_caches, :first_id
    add_index :strength_triangle_caches, :second_id

    create_table :individual_features_caches do |t|
      t.integer :first_id
      t.integer :second_id
      t.string :result

      t.timestamps
    end
    add_index :individual_features_caches, :first_id
    add_index :individual_features_caches, :second_id
  end
end
