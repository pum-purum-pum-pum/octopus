class PlayersController < ApplicationController
  before_action :set_player, only: [:show, :edit, :update, :destroy]

  # GET /players
  # GET /players.json
  def index
    @players = Player.search(params[:search])
                   .order('prize IS NULL ASC, prize DESC, rank IS NULL, rank ASC')
                   .paginate(page: params[:page])
  end

  # GET /players/1
  # GET /players/1.json
  def show
  end

  def load_suggestions
    @suggestions = Player
                       .search(params[:search])
                       .order('rank IS NULL, rank ASC, prize DESC')
                       .limit(30).select(:name, :oncourt_id)
    render json: @suggestions
  end

  def compare
    @first = Player.find_by_oncourt_id(params[:first_id])
    @second = Player.find_by_oncourt_id(params[:second_id])

    if @first.nil? or @first.rank.nil?
      redirect_back fallback_location: 'main#compare', notice: "Invalid id #{params[:first_id]}"
      return
    end
    if @second.nil? or @second.rank.nil?
      redirect_back fallback_location: 'main#compare', notice: "Invalid id #{params[:second_id]}"
      return
    end

    @infographics = Player.infographics(params[:first_id], params[:second_id])
    @infographics[:bookmakers]['data'].map! { |x| x.round(2) }
    @infographics[:individual_features]['data'].map! { |y| y.map! { |x| x.round(2) } }
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_player
      @player = Player.find_by_oncourt_id(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def player_params
      params.require(:player).permit(:oncourt_id, :name, :birthday, :country)
    end
end
