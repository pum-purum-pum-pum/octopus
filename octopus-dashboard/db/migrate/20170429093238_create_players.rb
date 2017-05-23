class CreatePlayers < ActiveRecord::Migration[5.0]
  def change
    create_table :players do |t|
      t.integer :oncourt_id
      t.string :name
      t.date :birthday
      t.string :country

      t.timestamps
    end

    add_index :players, :oncourt_id, unique: true
    add_index :players, :name
  end
end
