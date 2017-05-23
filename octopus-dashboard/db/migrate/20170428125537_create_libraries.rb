class CreateLibraries < ActiveRecord::Migration[5.0]
  def change
    create_table :libraries do |t|
      t.string :title
      t.string :author
      t.date :date_published

      t.timestamps
    end
  end
end
