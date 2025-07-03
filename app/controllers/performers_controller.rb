class PerformersController < ApplicationController
  def index
    @performers = Performer.all
  end

  def create
    performer_id = params[:performer_id]
    video_id = params[:video_id]
    if performer_id.present? && video_id.present?
      performance = Performance.create(performer_id: performer_id, video_id: video_id, date: Date.today)
      if performance.persisted?
        flash[:notice] = "パフォーマンスが登録されました。"
      else
        flash[:alert] = "パフォーマンスの登録に失敗しました。"
      end
    else
      flash[:alert] = "作業者または動画が選択されていません。"
    end
    redirect_to inputs_path
  end
end
