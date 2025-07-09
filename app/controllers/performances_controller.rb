class PerformancesController < ApplicationController
  def create

    performer_id = params[:performer_id]
    video_id = params[:video_id]
    averaged_results_path = session[:averaged_results_path]

    if performer_id.present? && video_id.present?
      performance = Performance.create(performer_id: performer_id, video_id: video_id, date: Date.today)
      if performance.persisted?
        if averaged_results_path && File.exist?(averaged_results_path)
          averaged_results = JSON.parse(File.read(averaged_results_path))
          averaged_results.each do |obj_id, values|
            values.each_with_index do |value, idx|
              Activity.create!(
                performance_id: performance.id,
                category: idx+1, 
                value: value
              )
            end
          end
        end
        flash[:notice] = "パフォーマンスとアクティビティが登録されました。"
      else
        flash[:alert] = "パフォーマンスの登録に失敗しました。"
      end
    else
      flash[:alert] = "作業者または動画が選択されていません。"
    end
    session.delete(:averaged_results_path)
    redirect_to inputs_path
  end
end
