class RenamePlayerColumn < ActiveRecord::Migration[5.0]
  def change
    rename_column :players, :birthday, :birthdate
  end
end
