require 'net/http'

class Player < ApplicationRecord
  def self.search(search)
    if search
      where(['name LIKE ?', "%#{search}%"]).where.not(rank: nil)
    else
      all.where.not(rank: nil)
    end
  end

  def self.infographics(first_id, second_id)
    prediction = Player.predict(first_id, second_id).to_f

    bookmakers = JSON.parse(Player.bookmakers(first_id, second_id))

    strength_polygon = Player.strength_triangle(first_id, second_id)
    if strength_polygon.blank?
      strength_polygon = nil
    else
      strength_polygon = JSON.parse(strength_polygon)
    end

    individual_features = JSON.parse(Player.individual_features(first_id, second_id))

    pair_features = JSON.parse(Player.pair_features(first_id, second_id))

    {
        prediction: prediction,
        bookmakers: bookmakers,
        strength_polygon: strength_polygon,
        individual_features: individual_features,
        pair_features: pair_features
    }
  end

  def self.bookmakers(first_id, second_id)
    cached = BookmakersCache.where(first_id: first_id, second_id: second_id).limit(1)
    if cached.empty?
      command = "http://localhost:5000/bookmakers?player1=#{first_id}&player2=#{second_id}"
      result = Net::HTTP.get(URI(command))

      BookmakersCache.create!(first_id: first_id, second_id: second_id, result: result)
    else
      result = cached.first.result
    end

    result
  end

  def self.strength_triangle(first_id, second_id)
    cached = StrengthTriangleCache.where(first_id: first_id, second_id: second_id).limit(1)
    if cached.empty?
      command = "python3 #{File.dirname(__FILE__)}/../../../octopus/Visualization/strength_triangle.py " +
          "--id1 #{first_id} --id2 #{second_id}"
      result = `#{python_virtualenv}#{command}`

      StrengthTriangleCache.create!(first_id: first_id, second_id: second_id, result: result)
    else
      result = cached.first.result
    end

    result
  end

  def self.individual_features(first_id, second_id)
    cached = IndividualFeaturesCache.where(first_id: first_id, second_id: second_id).limit(1)
    if cached.empty?
      command = "http://localhost:5000/win_rate?player1=#{first_id}&player2=#{second_id}"
      result = Net::HTTP.get(URI(command))

      IndividualFeaturesCache.create!(first_id: first_id, second_id: second_id, result: result)
    else
      result = cached.first.result
    end

    result
  end

  def self.predict(first_id, second_id)
    cached = PredictCache.where(first_id: first_id, second_id: second_id).limit(1)
    if cached.empty?
      command = "http://localhost:5000/prob?player1=#{first_id}&player2=#{second_id}"
      result = Net::HTTP.get(URI(command))

      PredictCache.create!(first_id: first_id, second_id: second_id, result: result)
    else
      result = cached.first.result
    end

    result
  end

  def self.pair_features(first_id, second_id)
    cached = PairFeaturesCache.where(first_id: first_id, second_id: second_id).limit(1)
    if cached.empty?
      command = "python3 #{File.dirname(__FILE__)}/../../../octopus/Visualization/players_pair_stats.py " +
          "--id1 #{first_id} --id2 #{second_id}"
      result = `#{python_virtualenv}#{command}`

      PairFeaturesCache.create!(first_id: first_id, second_id: second_id, result: result)
    else
      result = cached.first.result
    end

    result
  end

  private
  def self.python_virtualenv
    python_virtualenv = ''
    if ENV['OCTOPUS_VIRTUALENV'].present?
      python_virtualenv = ". #{ENV['OCTOPUS_VIRTUALENV']} && "
    end
    python_virtualenv
  end
end
