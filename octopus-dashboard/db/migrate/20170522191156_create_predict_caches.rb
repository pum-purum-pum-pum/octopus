class CreatePredictCaches < ActiveRecord::Migration[5.0]
  def change
    create_table :predict_caches do |t|
      t.integer :first_id
      t.integer :second_id
      t.string :result

      t.timestamps
    end

    add_index :predict_caches, :first_id
    add_index :predict_caches, :second_id
  end
end
