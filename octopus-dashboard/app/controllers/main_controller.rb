class MainController < ApplicationController
  def compare
  end

  def coming
    coming_games_ids = [
        [10014,29372],
        [24245,6820],
        [29732, 4061],
        [2123, 7459],
        [26923, 5054],
        [20648, 26900],
        [23142, 27482],
        [13445, 30470],
        [13957, 6850],
        [20104, 17359],
        [9488, 20104]

    ]

    @coming_games = coming_games_ids.map do |game_ids|
      prediction = Player.predict(game_ids[0], game_ids[1]).to_f
      {
          first_player: Player.find_by_oncourt_id(game_ids[0]),
          second_player: Player.find_by_oncourt_id(game_ids[1]),
          prediction: prediction,
          date: '24.05.2017'
      }
    end
  end
end
