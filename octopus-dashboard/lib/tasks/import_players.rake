require 'csv'
require 'activerecord-import'

namespace :import do
  desc 'Load players from players_atp.csv to AR database'
  task import_players: :environment do
    import_players
  end
end


def import_players
  players_csv = CSV.read("#{File.dirname(__FILE__)}/../../../octopus/data/dataset/players_atp.csv")

  players = []

  players_csv[1..-1].each do |row|
    birthdate = nil
    rank = nil
    if row[2]
      birthdate = Date.strptime(row[2], '%m/%d/%y')
    end
    if row[4]
      rank = row[4].to_i
    end

    unless row[1]['/'].nil?
      next
    end

    player = {oncourt_id: row[0].to_i, name: row[1],
              birthdate: birthdate, country: row[3],
              rank: rank, prize: row[15]}
    players.push player
  end

  p 'parsed'

  Player.delete_all
  p 'deleted'

  Player.import players
  p 'inserted'
end
