class AddPlayerColumns < ActiveRecord::Migration[5.0]
  def change
    add_column :players, :rank, :integer
    add_column :players, :prize, :integer
  end

  add_index :players, :rank
  add_index :players, :prize
end
